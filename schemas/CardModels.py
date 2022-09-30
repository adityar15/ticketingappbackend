from pydantic import BaseModel


class RequestModel(BaseModel):
    text: str
    category_id: int
    

class ResponseModel(BaseModel):
    id: int
    text: str
    rank: int
    category_id: int

    class Config(): 
        orm_mode = True