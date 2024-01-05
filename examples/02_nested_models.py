"""
Continuing the comparison, showcasing the insantiation of the nested models.
"""
from dataclasses import dataclass
from typing import Optional
from pydantic import BaseModel
import yaml


class Suitcase(BaseModel):
    items: list


class Human(BaseModel):
    name: str
    age: int
    suitcase: Optional[Suitcase]


# Create using 'regular' approach:
jan = Human(name="jan", age=6, suitcase=Suitcase(items=["comb", "toothbrush"]))
"""
>>> print(jan.json())
{"name": "jan", "age": 6, "suitcase": {"items": ["comb", "toothbrush"]}}
"""

# Create model from dict:
joe_d = {"name": "joe", "age": 6, "suitcase": {"items": ["comb", "toothbrush"]}}
joe = Human(**joe_d)
"""
>>> type(joe)
<class '__main__.Human'>
>>> type(joe.suitcase)
<class '__main__.Suitcase'>
"""

# Create model from YAML:
yaml_string = """
---
name:
  Janice
age:
  32
suitcase:
  items:
    - gloves
    - shoes  
"""
janice = Human(**yaml.safe_load(yaml_string))
"""
>>> type(janice)
<class '__main__.Human'>
"""

# creating nested dataclass does not have the same ergonomics:


@dataclass
class SuitcaseDC:
    items: list


@dataclass
class HumanDC:
    name: str
    age: int
    suitcase: Optional[SuitcaseDC]


joe_dc = HumanDC(**joe_d)
"""
>>> joe_dc
HumanDC(name='joe', age=6, suitcase={'items': ['comb', 'toothbrush']})
>>> type(joe_dc.suitcase)
<class 'dict'>                    # <<<< this is NOT a SuitcaseDC type
"""

# drop the validation for speed by using 'model_construct' (used to be 'construct' in v1):
input_d = {"name": "marie", "age": 2, "suitcase": {"items": ["comb", "toothbrush"]}}
marie = Human.model_construct(**input_d)
"""
>>> marie
Human(name='marie', age=2, suitcase={'items': ['comb', 'toothbrush']})
>>> type(marie)
<class '__main__.Human'>
>>> type(marie.suitcase) 
<class 'dict'>                      # <<<< OOps!
"""

# model_construct model WITHOUT validating data can also go wrong:
input_d = {
    "name": ["marie", "oops"],
    "age": 2,
    "suitcase": {"items": ["comb", "toothbrush"]},
}
marie_err = Human.model_construct(**input_d)
# notice how marie.name is now a list:
"""
>>> marie_err = Human.construct(**input_d)
>>> print(marie_err.json())
{"name": ["marie", "oops"], "age": 2, "suitcase": {"items": ["comb", "toothbrush"]}}
"""
