from pydantic import BaseModel , EmailStr , Field
from typing import Optional , Annotated
from datetime import datetime

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class UserResponse(BaseModel):
    id : int
    email : EmailStr

    model_config = {"from_attributes": True}

class Post(PostBase):
    id : int
    created_at : datetime
    owner_id : int
    owner : UserResponse

    model_config = {"from_attributes": True}

class UserCreate(BaseModel):
    email : EmailStr
    password : str

class UserLogin(BaseModel):
    email : EmailStr
    password : str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id : Optional[str] = None


class Vote(BaseModel):
    post_id : int
    dir : Annotated[int, Field(le=1)]


class PostOut(PostBase):
    post : Post
    votes : int

    model_config = {"from_attributes": True}





