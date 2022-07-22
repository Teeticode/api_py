from datetime import datetime
from pydantic import BaseModel, EmailStr, conint
from tokenize import String
from typing import Optional


# schemas
class PostBase(BaseModel):
    title: str
    content: str
    published: bool=True
    rating: Optional[int] = None
    postid: Optional[int]
    userid: Optional[int]

class CreateBase(PostBase):
    pass

class UpdateBase(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

class UserOut(BaseModel):
    email: EmailStr
    userid: int
    created_at: datetime

    class Config:
        orm_mode = True

# Our response schemas
class Post(PostBase):
    id:int
    created_at: datetime
    owner: UserOut

    class Config:
        orm_mode = True

class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        orm_mode = True
class PostUpdate(Post):
    pass

    class Config:
        orm_mode = True



# Users Base Schema

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    userid: Optional[int]
    



class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
class Token(BaseModel):
    token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None


# Vote schema

class Vote(BaseModel):
    postid: int
    dir: conint(le=1)# < = to 1
