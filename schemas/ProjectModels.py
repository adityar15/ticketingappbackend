from pydantic import BaseModel



class ResponseModel(BaseModel):
    id: int
    user_id: int
    title: str