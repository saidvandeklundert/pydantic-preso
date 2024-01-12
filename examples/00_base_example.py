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
jan.model_dump_json()
"""
>>> jan.json()
'{"name": "Jan", "age": 6}'
>>> jan.json(exclude={"age"})  
'{"name": "Jan"}'

>>> jan.schema()
{'description': 'A Pydantic Basemodel',
 'properties': {'name': {'title': 'Name', 'type': 'string'},
  'age': {'title': 'Age', 'type': 'integer'}},
 'required': ['name', 'age'],
 'title': 'Human',
 'type': 'object'}
 
>>> jan.dict()
{'name': 'Jan', 'age': 6}
>>> jan.dict(include={"name"}) 
{'name': 'Jan'}

# in v2:
>>> jan.model_dump_json()
'{"name":"Jan","age":6}'
"""
