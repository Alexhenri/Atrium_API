from pydantic import BaseModel


class ErrorSchema(BaseModel):
    # Defines how error msg will be presented  
    msg: str
