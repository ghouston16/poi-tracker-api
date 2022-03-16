from unicodedata import category
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

from pydantic.types import conint

## User Models

class UserCreate(BaseModel):
    email: EmailStr
    password: str

# Response Model - exclude password
class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True

# User Login class
class UserLogin(BaseModel):
    email = EmailStr
    password = str

# Category Model
class Category(BaseModel):
    name: str
    creator: int

# Response Model
class CategoryOut(Category):
    id: int
    created_at: datetime
    class Config: 
        orm_mode = True

# Poi Model
class PoiBase(BaseModel):
    title: str
    description: str
    category: Optional[int]
    lat: str
    lng: str
    published: bool = True
    creator: int

class PoiCreate(PoiBase):
    pass

# Response Model
class Poi(PoiBase):
    id: int
    created_at: datetime
    owner: UserOut
    class Config: 
        orm_mode = True

# Access Token Model
class Token(BaseModel):
    access_token: str
    token_type: str

# Token data model
class TokenData(BaseModel):
    id: Optional[str] = None

# Like Model
class Like(BaseModel):
    poi_id:int
    dir: conint(le=1)

class PoiOut(BaseModel):
    Poi: Poi
    likes: int
    class Config: 
        orm_mode = True

class Comment(BaseModel):
    comment: str
    published: bool = True
    poi_id: int
    creator: int

class CommentOut(Comment):
    id: int
    created_at: datetime
    owner: UserOut
    parent: Poi
    class Config: 
        orm_mode = True
