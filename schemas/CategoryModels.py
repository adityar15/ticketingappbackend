from pydantic import BaseModel
from .CardModels import ResponseModel as CardModel
from typing import List

class RequestModel(BaseModel):
    title: str
    color: str


class ResponseModel(BaseModel):
    id: int
    title: str
    color: str
    project_id: int
    cards: List[CardModel]

    class Config:
        orm_mode = True