"""
It is possible, perhaps not recommended, to create models at runtime. 

Those models are also validated.
"""
from pydantic import create_model

fields = {'name': (str, ...), 'age': (int, ...)}
DynamicModel = create_model('DynamicModel', **fields)

jan = DynamicModel(name="Jan", age=8)
print(jan.model_dump_json())

try:
    DynamicModel(name="Jan", age=[1,2,3])
except Exception as err:
    print(err)