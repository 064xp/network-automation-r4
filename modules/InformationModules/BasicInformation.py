from typing import cast
from .InformationModule import InformationModule
from ..NetDevice import NetDevice


class BasicInformation(InformationModule):
    '''
    Gets hostname and domain name of a net device
    '''

    def getInfo(self, netDevice: NetDevice):
        netDevice.conn.enable()
        domainInfo = cast(str, netDevice.conn.send_command(
            "show run | include ip domain name"))
        hostnameInfo = cast(str, netDevice.conn.send_command(
            "show run | include hostname"))
        domain = ""
        hostname = ""

        if len(domainInfo) > 0:
            domain = domainInfo.split(' ')[-1]

        if len(hostnameInfo) > 0:
            hostname = hostnameInfo.split(' ')[-1]

        netDevice.domainName = domain
        netDevice.hostname = hostname

    def moduleSupported(self, netDevice: NetDevice) -> bool:
        # If it already has domain or hostname, no need to run the module on it
        if netDevice.domainName == "" or netDevice.hostname == "":
            return True
        return False
