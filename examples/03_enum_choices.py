"""
In addition to allowing nested types, Enums can be used to enumerate and enforce choices.

With string inputs, Pydantic will validate it against what is permitted according to the Enum.
"""
from enum import Enum

from pydantic import BaseModel, ValidationError


class Vendor(str, Enum):
    CISCO = "cisco"
    ARISTA = "arista"
    JUNIPER = "juniper"




class Router(BaseModel):
    model: Vendor = Vendor.CISCO
    


print(Router())
"""
>>> model=<Vendor.CISCO: 'cisco'>
"""
print(Router(model="juniper"))
"""
>>> model=<Vendor.JUNIPER: 'juniper'>
"""
try:
    Router(model="a")
except ValidationError as e:
    print(e)
    """
    ValidationError: 1 validation error for Router
    model
    Input should be 'cisco','arista' or 'juniper' [type=enum, input_value='a', input_type=str]
    """
