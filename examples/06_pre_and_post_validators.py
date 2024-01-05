"""
Massaging data before and after instantiation.
"""
from pydantic import BaseModel, model_validator
from typing import Any

class NetworkDevice(BaseModel):
    """
    Representation of a NetworkDevice
    """
    hostname: str

        
    @model_validator(mode='before')
    @classmethod
    def sanitize_hostname(cls, data: Any) -> Any:
        """
        Preprocessing raw data.
        """
        print(f"data send into the mode: {data}")
        data["hostname"] = data["hostname"].strip().lower() 
        return data

router_1 = NetworkDevice(hostname="RouteR-1")
print(router_1.model_dump_json())