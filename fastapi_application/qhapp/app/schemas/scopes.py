import uuid

from pydantic import BaseModel, Field, ConfigDict

class ScopeCreate(BaseModel):
    uuid: uuid.UUID
    name: str = Field(..., min_length=3, max_length=64)
    
class ScopeRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    uuid: uuid.UUID
    name: str