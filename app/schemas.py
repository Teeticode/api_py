from datetime import datetime
from pydantic import BaseModel
from tokenize import String
from typing import Optional


# schemas
class PostBase(BaseModel):
    title: str
    content: str
    published: bool=True
    rating: Optional[int] = None
    postid: Optional[int]

class CreateBase(PostBase):
    pass

class UpdateBase(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


# Our response schemas
class Post(PostBase):
    created_at: datetime

    class Config:
        orm_mode = True
    
class PostUpdate(Post):
    pass

    class Config:
        orm_mode = True