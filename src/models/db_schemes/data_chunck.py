from pydantic import BaseModel, Field , validator   
from bson.objectid import ObjectId
from typing import Optional


class DataChunk(BaseModel):
    _id: Optional[ObjectId]
    chunk_text: str = Field(... , min_length=1) 
    chunk_metdata : dict
    chunk_oreder: int = Field(... , gt=0)
    chunk_peoject_id: ObjectId
    

    class Config:
        arbitrary_types_allowed = True