from pydantic import BaseModel
from enum import Enum


class Vendor(str, Enum):
    CISCO = "cisco"
    ARISTA = "arista"
    JUNIPER = "juniper"




class Router(BaseModel):
    model: Vendor = Vendor.CISCO

    class Config:
        use_enum_values = False
        validate_default=True

class RouterEnumValues(BaseModel):
    model: Vendor = Vendor.CISCO

    class Config:
        """
        Output the value of the Enum in any type of serialization.

        The validate_default is set to also apply this to default arguments.
        """
        use_enum_values = True
        validate_default=True







cisco_enum_false = Router()
cisco_enum_true = RouterEnumValues()

print(cisco_enum_false.model_dump())
print(cisco_enum_true.model_dump())
