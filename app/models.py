from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

from .database import Base
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import INT, TIMESTAMP, Boolean
from .database import Base
from sqlalchemy import Column, Integer, String, Boolean


# Base Model for Poi
class Poi(Base):
    __tablename__ = "pois"
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    lat = Column(String, nullable=True)
    lng = Column(String, nullable=True)
    category = Column(Integer, nullable=True)
    published = Column(Boolean, server_default="TRUE", nullable=False)
    creator = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    # SQLAlchemy will recognise relationship once defined
    owner = relationship("User")


# Define User model
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )


# Likes model added
class Like(Base):
    __tablename__ = "likes"
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    poi_id = Column(
        Integer, ForeignKey("pois.id", ondelete="CASCADE"), primary_key=True
    )


# Comment Model
class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    comment = Column(String, nullable=False)
    poi_id = Column(Integer, ForeignKey("pois.id", ondelete="CASCADE"), nullable=False)
    published = Column(Boolean, server_default="TRUE", nullable=False)
    creator = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    # SQLAlchemy will recognise relationship once defined
    parent = relationship("Poi")
    owner = relationship("User")


# Category Model
class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String, nullable=False)
    creator = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=True)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
