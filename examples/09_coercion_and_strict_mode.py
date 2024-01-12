"""
Pydantic will attempt to coerce one type into another.

Most oftentimes, this is great!

For instance, with Enums, UUIDs, IP addresses and more.

However, in some cases, you might not want this. If this is the case, strict mode has you covered.

"""
from uuid import UUID
import ipaddress
from enum import Enum

from pydantic import BaseModel, ValidationError

class Brand(Enum):
    BMW= "bmw"
    VOLKSWAGEN= "volkswagen"


class SomeModel(BaseModel):
    uuid: UUID
    address: ipaddress.IPv4Interface
    brand:Brand

some_model = SomeModel(uuid="177ef0d8-6630-11ea-b69a-0242ac130003", address="1.1.1.1/32", brand="volkswagen")
print(some_model.model_dump_json(indent=2))
    
try:
    another_instantiation = SomeModel.model_validate({"uuid":"177ef0d8-6630-11ea-b69a-0242ac130003", "address":"1.1.1.1/32", "brand":"volkswagen"}, strict=True)
except Exception as err:
    print("Failed to create SomeModel with strict mode")

another_instantiation = SomeModel.model_validate({"uuid":UUID("177ef0d8-6630-11ea-b69a-0242ac130003"), "address":ipaddress.IPv4Interface("1.1.1.1/32"), "brand":Brand.VOLKSWAGEN}, strict=True)

print(f"Created model using strict mode after passing in the proper types:\n{another_instantiation.model_dump_json(indent=3)}")