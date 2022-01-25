from unicodedata import category
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

from pydantic.types import conint

# Post Model
class PostBase(BaseModel):
    title: str
    description: str
    lat: str
    long: str
    category: str
    published: bool = True

class PostCreate(PostBase):
    pass

# Response Model
class Post(PostBase):
    id: int
    created_at: datetime


class PostOut(BaseModel):
    Post: Post

