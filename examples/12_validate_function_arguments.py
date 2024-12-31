"""
Using Pydantic to validate function calls at runtime.
"""
from typing import Annotated, Literal
from pydantic import Field, ValidationError, validate_call

## simple validation:
NonEmptyString = Annotated[str,Field(min_length=1)]

@validate_call
def extract_a_char(s:NonEmptyString)->str:
    return s[0]

extract_a_char("this works")
try:
    extract_a_char("")
except ValidationError as err:
    print(f"caught a ValidationError raised by extract_a_char:\n{str(err)}")


# constraining input:
ActionType = Literal["START", "STOP"]

@validate_call
def do_something(action: ActionType) -> str:
    return f"Performing action: {action}"


# more complex validation:
from typing import Annotated
from pydantic import Field, ValidationError, validate_call, BeforeValidator

def validate_no_q(v: str) -> str:
    """
    Verify that the letter q does not appear in a string.
    """
    if 'q' in v.lower():
        raise ValueError("The string must not contain the letter 'q'")
    return v

def validate_no_z(v: str) -> str:
    """
    Verify that the letter z does not appear in a string.
    """
    if 'z' in v.lower():
        raise ValueError("The string must not contain the letter 'z'")
    return v


NonEmptyStringExtended = Annotated[
    str,
    Field(min_length=1),
    BeforeValidator(validate_no_q),
    BeforeValidator(validate_no_z)
]

@validate_call
def extract_a_char(s: NonEmptyStringExtended) -> str:
    return s[0]

extract_a_char("aza")