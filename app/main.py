from fastapi import Depends, FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session

from app.config import settings
from . import models
from .database import engine, get_db
from passlib.context import CryptContext
from .routers import poi, user

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

while True:
    try:
            conn = psycopg2.connect(host=settings.database_hostname, database=settings.database_name,user=settings.database_username,password=settings.database_password, cursor_factory=RealDictCursor)
            cursor = conn.cursor()
            print('DB connection success')
            break
    except Exception as error: 
            time.sleep(5)
            print('Error connecting to Db')

 # Include Routers
app.include_router(poi.router)
app.include_router(user.router)

@app.get("/sqlalchemy")
def test_pois(db: Session = Depends(get_db)):
    return {"status": "success"}


@app.get("/")
def root():
    return {"message": "Welcome to my Python API"}

