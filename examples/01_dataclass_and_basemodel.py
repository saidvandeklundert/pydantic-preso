"""
Comparing a dataclass to a Pydantic BaseModel

Emphasizing the fact that Pydantic validates the type hints at runtime.
"""
from dataclasses import dataclass
from pydantic import BaseModel


@dataclass
class HumanDataClass:
    name: str
    age: int


class HumanBaseModel(BaseModel):
    name: str
    age: int


if __name__ == "__main__":
    anita = HumanDataClass(name="Anita", age=[0])
    anita.age
    human_1_1 = HumanDataClass(name="Jan", age=6)
    human_1_1.age

    human_1_2 = HumanBaseModel(name="Jan", age=6)
    
    # notice we can instantiate the dataclass with the wrong type:
    human_2_1 = HumanDataClass(name="Jan", age="Six")


    try:
        # Pydantic validates the type at runtime:
        human_2_2 = HumanBaseModel(name="Jan", age="six")
    except Exception as err:
        print(err)

"""
ValidationError: 1 validation error for HumanBaseModel
age
  Input should be a valid integer, unable to parse string as an integer [type=int_parsing, input_value='six', input_type=str]
    For further information visit https://errors.pydantic.dev/2.3/v/int_parsing
"""