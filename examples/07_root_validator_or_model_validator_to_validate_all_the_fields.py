"""
The 'model_validator' (root validator in v1) is another powerful concept. 


The annotated validator method will give you access to all the fields in the class and it allows
you to take all the field values into consideration.

In this example, I use the model_validator to:
- ensure certain fields are not passed into the model
- ensure the hostname of the router is also part of another field name
- ensure the IP addresses assigned to the router and the interface model that is embedded
 in the router are unique and not overlapping
"""
from pydantic import BaseModel, ValidationError, model_validator
import ipaddress
from typing import Union, Any, List
import itertools


def check_network_membership(
    network_1: Union[str, ipaddress.IPv4Network],
    network_2: Union[str, ipaddress.IPv4Network],
) -> bool:
    """
    Check if network_1 is in network_2.

    Examples:
    >>> check_network_membership("2.2.2.2/32", "1.0.0.0/24") -> False
    >>> check_network_membership("1.0.0.2/32", "1.0.0.0/24") -> True
    """
    overlap = ipaddress.ip_network(network_2).overlaps(ipaddress.ip_network(network_1))
    if overlap is True:
        print(f"{network_1} is in {network_2}")
    return overlap

class Interface(BaseModel):
    """
    An interface on a NetworkDevice
    """
    interface_name: str
    ipv4: Union[ipaddress.IPv4Interface, None] = None
    ipv6: Union[ipaddress.IPv6Interface, None] = None

class NetworkDevice(BaseModel):
    """
    Representation of a NetworkDevice
    """
    fqdn_name:str
    hostname: str
    role: str
    username: str
    password:str
    site: str
    mgmt_ip : ipaddress.IPv4Interface
    interfaces : List[Interface] = []

    @model_validator(mode="before")
    @classmethod
    def ensure_field_name_does_not_exist(cls, data: Any)->Any:
        """
        This method runs before Pydantic tries to instantiate the instance.

        You have access to the fields and you can verify or maniplate the data that 
        is being unsed to creat this instance.

        In this example, we ensure that the value 'illegal_field' is not present
        when we create this instance.
        """
        if isinstance(data, dict):
            assert (
                'illegal_field' not in data
            ), 'illegal_field should not be included'
        return data
    
    @model_validator(mode="after")
    def check_fqdn_name(self):
        """
        This method runs after we instantiate a Pydantic Basemodel.

        Here we can do the validation by simply refering to the fields using self.
        """
        hostname = self.hostname
        fqdn_name = self.fqdn_name         
        if hostname not in fqdn_name:
            raise ValueError(f'hostname {hostname} must be included in fqdn_name {fqdn_name}.')

        return self
    
    @model_validator(mode="after")
    def check_ipv4_overlap(self):
        """
        This method runs after we instantiate a Pydantic Basemodel.

        We validate whether or not IP address overlap exists.

        This is just an example. Normally, the Network class would validated all interfaces
        in the network to ensure there is no overlap.
        ip2.network.overlaps(ip.network)
        """
        all_ip_addresses = set()
        all_ip_addresses.add(self.mgmt_ip)
        for interface in self.interfaces:
            if interface.ipv4 in all_ip_addresses:
                raise ValueError(f"duplicate IP on interface {interface.interface_name}")
            all_ip_addresses.add(interface.ipv4)
        for ip1, ip2 in itertools.combinations(list(all_ip_addresses), 2):            
            if ip1.network.overlaps(ip2.network):
                raise ValueError(f"Overlapping IPs detected:{ip1.network} and {ip2.network}")
        return self    

router_1 = {
    "hostname":"router-1",
    "fqdn_name":"router-1.example.com",
    "role": "dar",
    "username":"said",
    "password": "lovely",
    "site":"dal09",
    "mgmt_ip":"1.1.1.1/32",
}

router_2 = {
        "hostname":"router-2",
        "fqdn_name":"router-1.example.com",
        "role": "dar",
        "username":"said",
        "password": "lovely",
        "site":"dal09",
        "mgmt_ip":"1.1.1.1/32",
}

router_3 = {
        "hostname":"router-3",
        "fqdn_name":"router-3.example.com",
        "role": "dar",
        "username":"said",
        "password": "lovely",
        "site":"dal09",
        "mgmt_ip":"1.1.1.1/32",
        "interfaces": [{"interface_name": "some_name", "ipv4":"2.0.0.0/30"}]
}

router_4 = {
        "hostname":"router-4",
        "fqdn_name":"router-4.example.com",
        "role": "dar",
        "username":"said",
        "password": "lovely",
        "site":"dal09",
        "mgmt_ip":"1.1.1.1/32",
        "interfaces": [{"interface_name": "some_name", "ipv4":"1.0.0.0/30"}]
}

router_5 = {
        "hostname":"router-5",
        "fqdn_name":"router-5.example.com",
        "role": "dar",
        "username":"said",
        "password": "lovely",
        "site":"dal09",
        "mgmt_ip":"1.1.1.1/32",
        "interfaces": [{"interface_name": "some_name", "ipv4":"2.1.1.0/30"},{"interface_name": "duplicate_ip", "ipv4":"1.1.1.1/32"}]
}

router_6 = {
        "hostname":"router-6",
        "fqdn_name":"router-6.example.com",
        "role": "dar",
        "username":"said",
        "password": "lovely",
        "site":"dal09",
        "mgmt_ip":"1.1.1.1/32",
        "interfaces": [{"interface_name": "overlap", "ipv4":"1.1.1.0/30"}]
}

routers = [router_1, router_2, router_3, router_4, router_5, router_6]

for router in routers:
    try:

        device = NetworkDevice(**router)
        print(f"{device.hostname} instantiated succesfully!\n")
    except ValidationError as e:
        print(f"{router['hostname']} instantiation failed:\n")
        print(e, "\n")