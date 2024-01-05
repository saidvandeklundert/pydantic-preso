"""
Pydantic has the concept of validators.

The 'regular' Pydantic checks the 'mechanical' value.

The validators allow you to put in semantic checks.

To use the validator:
- annotate a method with the validator decorator
- reference the field value you want to decorate
- put in place the logic and checks
- can use simple assertions or implement whatever python you can think of
"""
from pydantic import BaseModel, ValidationError, validator


class InputValues(BaseModel):

    vlan: int

    @validator("vlan")
    def vlan_validator(cls, v):
        assert v >= 1, "invalid vlan number, number too low"
        assert v <= 4094, "invalid vlan number, number too high"
        return v


"""
>>> _2000 = InputValues(vlan=2000)
>>> 
>>> try:
...     _6000 = InputValues(vlan=6000)
... except ValidationError as e:
...     print(e)
... 
1 validation error for InputValues
vlan
  invalid vlan number, number too high (type=assertion_error)
>>>
"""


# For simple things, there are also some config options:
class SomeModel(BaseModel):
    v: str

    class Config:
        str_max_length = 5


one = SomeModel(v="one")
thirtyfive = SomeModel(v="thirtyfive")
"""
ValidationError: 1 validation error for SomeModel
v
  String should have at most 5 characters [type=string_too_long, input_value='thirtyfive', input_type=str]
    For further information visit https://errors.pydantic.dev/2.3/v/string_too_long
"""


# We can also validate fields based on the values assigned to other fields.
#
from pydantic import BaseModel, ValidationError, validator


class Person(BaseModel):
    name: str
    age: int
    drivers_license: bool

    @validator("drivers_license")
    def drivers_license_age(cls, v, values):
        if v is True and values["age"] < 18:
            raise ValueError("Drivers license before the age of 18 is not possible in the Netherlands!")
        return v

# valid combination:
marie = Person(
    name="Marie",
    age=5,
    drivers_license=False,
)


# invalid combination, and thuse fails the validation:
try:
    Person(
        name="Jan",
        age=6,
        drivers_license=True,
    )
except ValidationError as e:
    print(e)
