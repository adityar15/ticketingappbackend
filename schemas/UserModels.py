from typing import List, Union, Optional
from pydantic import BaseModel, EmailStr, validator


class RequestModel(BaseModel):
    name: str
    email: EmailStr
    password: str
    confirm_password: str

    @validator('password')
    def validatePassword(cls, value):
        if len(value) < 3 or len(value) > 16:
            raise ValueError('password length must be in the range of 3 - 16 characters')
        
        assert value.isalnum(), 'password must be alphanumeric'
        return value
    
    @validator('confirm_password')
    def validateConfirmPassword(cls, value, values, **kwargs):
         if 'password' in values and value != values['password']:
            raise ValueError('passwords do not match')
         return value



class LoginRequestModel(BaseModel):
    email: EmailStr
    password: str



class ResponseModel(BaseModel):
    id: int
    name: str
    email: EmailStr

