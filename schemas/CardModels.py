from pydantic import BaseModel
from typing import Optional

class RequestModel(BaseModel):
    text: str
    category_id: int
    rank: int

class UpdateTextModel(BaseModel):
    text: str
    card_id: int


class UpdateRankModel(BaseModel):
    id: int
    text: str
    category_id: int
    rank: int

class DeleteModel(BaseModel):
    card_id: int

class ResponseModel(BaseModel):
    id: int
    text: str
    rank: int
    category_id: int

    class Config(): 
        orm_mode = True