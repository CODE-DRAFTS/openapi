from pydantic import BaseModel,EmailStr
from datetime import datetime


class PostBase(BaseModel):
    title :  str
    content: str
    published: bool =True


class CreatePost(PostBase):
    pass


class Post(BaseModel):
    title: str
    content: str
    published: bool

class NewUser(BaseModel):
    email: EmailStr
    password: str

class ResponseGetUSer(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
