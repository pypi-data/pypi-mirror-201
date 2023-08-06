import json

import requests
import os


class HeartBeat:
    client_Token = None
    authorization_key = None

    def client(self, access_key, access_token):
        global client_Token, authorization_key
        client_Token = access_key
        authorization_key = access_token
        return HeartBeat()

    def upload_file(self, path=None):
        url = 'https://ze3uixrwii.execute-api.ap-south-1.amazonaws.com/Prod/get-upload-url'
        headers = {
            'clientToken': client_Token,
            'AuthorizationKey': authorization_key
        }
        filename = os.path.basename(path)
        body = {
            'fileName': filename
        }
        response = requests.post(url, headers=headers, data=json.dumps(body)).json()
        UUID = {'fileName':path, 'UUID': response.get('UUID')}
        if response.get('statusCode') != 200:
            return response
        with open(path, 'rb') as file:
            file_response = requests.put(response.get('presignedUrl'), data=file.read())
        return {'status': 200, 'message': 'Folder Successfully uploaded to S3', 'info': UUID}

    def upload_folder(self, path=None):
        url = 'https://ze3uixrwii.execute-api.ap-south-1.amazonaws.com/Prod/get-upload-url'
        headers = {
            'clientToken': client_Token,
            'AuthorizationKey': authorization_key
        }
        root_folder = os.path.dirname(path)
        arr = []
        for root, dirs, files in os.walk(path):
            for file in files:
                file_path = os.path.join(root, file)
                file_name = ''
                if os.path.dirname(file_path) != root_folder:
                    file_name = os.path.dirname(file_path).replace(root_folder+'/', '')+'/'+file
                else:
                    file_name = os.path.basename(file_path)

                body = {
                    'fileName': file_name
                }
                response = requests.post(url, headers=headers, data=json.dumps(body)).json()
                UUID = {'fileName':file_path, 'UUID': response.get('UUID')}
                arr.append(UUID)
                if response.get('statusCode') != 200:
                    return response
                with open(file_path, 'rb') as file:
                    file_response = requests.put(response.get('presignedUrl'), data=file.read())

        return {'status': 200, 'message': 'Folder Successfully uploaded to S3', 'info': arr}
