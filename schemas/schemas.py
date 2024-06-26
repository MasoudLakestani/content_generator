from typing import List, Optional
from pydantic import BaseModel # type: ignore

class Parameter(BaseModel):
    subject:str
    keywords: Optional[List[str]]
    tone:int=1
    brand_name:Optional[str] = None

class UserBase(BaseModel):
    username:str
    email:str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    api_key: str

    class Config:
        from_attributes=True