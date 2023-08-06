from heartbeat.heartbeat import HeartBeat

__version__ = "0.1.0"
__author__ = 'Shubham  Kumar'
__credits__ = 'Ioanyt Innovations Pvt. Ltd'


def client(clientToken, authorizationKey):
    """
    Create a low-level service client by name using the default session.

    See :py:meth:`heartbeat`.
    """
    client_obj = HeartBeat()
    return client_obj.client(clientToken, authorizationKey)
