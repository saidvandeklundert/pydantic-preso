"""
No frills example of a BaseModel.
"""
from pydantic import BaseModel


class Human(BaseModel):
    """
    A Pydantic Basemodel
    """
    name: str
    age: int


jan = Human(name="Jan", age=6)

"""
>>> jan.json()
'{"name": "Jan", "age": 6}'
>>> jan.json(exclude={"age"})  
'{"name": "Jan"}'

>>> jan.dict()
{'name': 'Jan', 'age': 6}
>>> jan.dict(include={"name"}) 
{'name': 'Jan'}
"""
# can construct from dict, will ignore unspecified fields:
marie = Human.parse_obj({"name": "marie", "age": 4, "child": True})
