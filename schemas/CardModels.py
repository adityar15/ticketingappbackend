from pydantic import BaseModel
from typing import Optional

class RequestModel(BaseModel):
    text: str
    category_id: int
    rank: int

class UpdateModel(BaseModel):
    text: Optional[str]
    category_id: Optional[int]
    rank: Optional[int]
    card_id: int

class DeleteModel(BaseModel):
    card_id: int

class ResponseModel(BaseModel):
    id: int
    text: str
    rank: int
    category_id: int

    class Config(): 
        orm_mode = True