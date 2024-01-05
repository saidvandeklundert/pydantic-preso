"""
Pydantic BaseModels are 'just classes'.

You can use them in ABC, bolt on properties, add user-defined methods and 'whatever'
"""
from abc import ABC, abstractmethod
from pydantic import BaseModel, computed_field
from enum import Enum
import ipaddress

class Os(Enum):
    EOS = "eos"
    JUNOS = "junos"
    IOSXE = "iosxe"

class NetworkDevice(ABC, BaseModel):
    
    hostname:str
    os : Os

    @computed_field
    @property
    def fqdn_name(self)->str:
        return f"{self.hostname}.example.come"
    
    @abstractmethod
    def register_with_monitoring_system(self):
        pass

    
    def is_registered_in_all_systems(self):
        print("monitoring - check")
        print("inventory - check")
        print("observed state - device not found!")



class Router(NetworkDevice):

    loopback:ipaddress.IPv4Interface

   
    def register_with_monitoring_system(self):
        print("registering data with monitoring system")
        print(self.model_dump_json(indent=2))

class Switch(NetworkDevice):

    vlan_interface:ipaddress.IPv4Interface
    mgmt_vlan:int

    
    def register_with_monitoring_system(self):
        print("registering data with monitoring system")
        print(self.model_dump_json(indent=2))


r1 = Router(hostname="router-1", os=Os.JUNOS, loopback="1.1.1.1/32")
switch1 = Switch(hostname="switch-1", os=Os.EOS, vlan_interface="1.1.1.1/32",mgmt_vlan=1)


devices = [r1, switch1]

def device_handler(devices:list[NetworkDevice]):
    for device in devices:
        device.register_with_monitoring_system()
        device.is_registered_in_all_systems()

device_handler(devices=devices)