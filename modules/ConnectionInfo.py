from typing import Union
from netmiko import ConnectHandler, BaseConnection


class ConnectionInfo:
    def __init__(self, host: str, user: str, password: str, secret: str):
        self.host = host
        self.user = user
        self.password = password
        self.secret = secret
        conn: Union[BaseConnection, None] = None

    def __getstate__(self):
        state = self.__dict__.copy()
        del state['conn']
        return state

    def connect(self):
        router = {
            'device_type': 'cisco_ios',
            'host':   self.host,
            'username': self.user,
            'password': self.password,
            'secret': self.secret
        }

        self.conn = ConnectHandler(**router)
