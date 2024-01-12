"""
Alias field names when serializing and deserializing.



"""
from pydantic import BaseModel, Field


"""
Say external applications are camelcasing your input:
"""


class SomeModelSerializationAlias(BaseModel):
    """
    Define a model with an aliased field name
    """
    field_name: str = Field(..., serialization_alias='FieldName')

# instantiate with the alias:
some_other_model = SomeModelSerializationAlias(field_name='johndoe')  

print(f"we access the field by using some_model.field_name: {some_other_model.FieldName}")
# serialize with or without the alias:
print(some_other_model.model_dump_json(indent=3))
print(some_other_model.model_dump_json(indent=3, by_alias=True))


"""
Perhaps you want to emit camelcase and use it during instantiation, but not internally in the code base:
"""
class SomeModel(BaseModel):
    """
    Define a model with an aliased field name
    """
    field_name: str = Field(..., alias='FieldName')

# instantiate with the alias:
some_model = SomeModel(FieldName='johndoe')  

print(f"we access the field by using some_model.field_name: {some_model.field_name}")
# serialize with or without the alias:
print(some_model.model_dump_json(indent=3))
print(some_model.model_dump_json(indent=3, by_alias=True))




"""
Perhaps you only take in an alternate field name, but you do not want to serialize it or use it anywhere:
"""
class SomeModel(BaseModel):
    """
    Define a model with an aliased field name
    """
    field_name: str = Field(..., validation_alias='FieldName')

# instantiate with the alias:
some_model = SomeModel(FieldName='johndoe')  

print(f"we access the field by using some_model.field_name: {some_model.field_name}")
# serialize with or without the alias:
print(some_model.model_dump_json(indent=3))
print("Notice in the following, we set alias to True, but for the field with 'validation_alias' this is ignored:")
print(some_model.model_dump_json(indent=3, by_alias=True))




