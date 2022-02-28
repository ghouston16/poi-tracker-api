from fastapi import Depends, FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session

from app.config import settings
from . import models
from .database import engine, get_db
from passlib.context import CryptContext
from .routers import poi, user, authenticate, likes
from fastapi.middleware.cors import CORSMiddleware
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

app = FastAPI()

# Obselete with Alembic
#models.Base.metadata.create_all(bind=engine)

# Change this to Web App URL
origins = ["*"]

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

 # Include Routers
app.include_router(poi.router)
app.include_router(user.router)
app.include_router(authenticate.router)
app.include_router(likes.router)

@app.get("/sqlalchemy")
def test_pois(db: Session = Depends(get_db)):
    return {"status": "success"}


@app.get("/")
def root():
    return {"message": "Welcome to my Python API"}

