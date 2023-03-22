from typing import Union
from netmiko import ConnectHandler, BaseConnection


class ConnectionInfo:
    host = ""
    user = ""
    password = ""
    secret = ""
    conn: Union[BaseConnection, None] = None

    def __init__(self, host: str, user: str, password: str, secret: str):
        self.host = host
        self.user = user
        self.password = password
        self.secret = secret

    def connect(self):
        router = {
            'device_type': 'cisco_ios',
            'host':   self.host,
            'username': self.user,
            'password': self.password,
            'secret': self.secret
        }

        self.conn = ConnectHandler(**router)
