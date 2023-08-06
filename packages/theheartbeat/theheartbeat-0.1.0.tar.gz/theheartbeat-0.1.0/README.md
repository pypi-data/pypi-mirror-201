# HeartBeat
A Python module for uploading files and folders to Amazon S3.

# Installation

You can install HeartBeat using pip:

```bash
pip install heartbeat
```
# Usage
 ```python
import heartbeat

access_key = 'your_access_key'
access_token = 'your_access_token'

# create a client object
client = heartbeat.client(access_key, access_token)

# upload a file
response = client.upload_file('/path/to/file')
print(response)

# upload a folder
response = client.upload_folder('/path/to/folder')
print(response)
```
# API Reference
### 'client(clientToken, authorizationKey)'
Create a client object for HeartBeat.

### Parameters:

- 'clientToken' (str): The client token for authentication.
- 'authorizationKey' (str): The authorization key for authentication.
### Returns:

- 'HeartBeat': The client object for uploading files and folders to Amazon S3.
### 'upload_file(path)'
Upload a file to Amazon S3.

#### Parameters:

- 'path' (str): The path to the file to upload.
#### Returns:

- 'dict': A dictionary with information about the uploaded file.
### 'upload_folder(path)'
Upload a folder and its contents to Amazon S3.

#### Parameters:

- 'path' (str): The path to the folder to upload.
#### Returns:

- 'dict': A dictionary with information about the uploaded folder and its contents.
# License
This project is licensed under the MIT <ins>License</ins> - see the LICENSE file for details.