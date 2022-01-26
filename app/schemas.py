from unicodedata import category
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

from pydantic.types import conint

# Poi Model
class PoiBase(BaseModel):
    title: str
    description: str
    category: str
    lat: str
    long: str
    published: bool = True

class PoiCreate(PoiBase):
    pass

# Response Model
class Poi(PoiBase):
    id: int
    created_at: datetime
    class Config: 
        orm_mode = True

class PoiOut(BaseModel):
    Poi: Poi
    class Config: 
        orm_mode = True

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
