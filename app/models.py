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



class Poi(Base):
    __tablename__ = "pois"
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    lat = Column(String, nullable=True)
    lng = Column(String, nullable=True)
    category =  Column(String, nullable=True)
    published = Column(Boolean, server_default='TRUE', nullable=False)
    creator = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    # SQLAlchemy will recognise relationship once defined
    owner = relationship("User")


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))

# Likes model added 
class Like(Base):
    __tablename__= "likes"
    user_id= Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    poi_id= Column(Integer,ForeignKey("pois.id", ondelete="CASCADE"), primary_key=True)