from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class UserOut(BaseModel):
    id: int
    email: EmailStr

    class Config:
        orm_mode = True

class Post(BaseModel):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut
    class Config:
        orm_mode = True



class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class CreatePost(BaseModel):
    pass


class UserCreate(BaseModel):
    email: EmailStr
    password: str





class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None