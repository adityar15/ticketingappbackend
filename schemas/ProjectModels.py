from pydantic import BaseModel
from .CategoryModels import ResponseModel as CategoryResponseModel
from typing import List

class RequestModel(BaseModel):
    user_id: int
    title: str

class ResponseModel(BaseModel):
    id: int
    user_id: int
    title: str
    categories: List[CategoryResponseModel]

    class Config:
        orm_mode = True