from fastapi import Depends, FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session

from app.config import settings
from . import models
from .database import engine, get_db
from passlib.context import CryptContext
from .routers import poi, user, authenticate
from fastapi.middleware.cors import CORSMiddleware
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

app = FastAPI()

# Obselete with Alembic
#models.Base.metadata.create_all(bind=engine)
'''
while True:
    try:
            conn = psycopg2.connect(host=settings.database_hostname, database=settings.database_name,user=settings.database_username,password=settings.database_password, cursor_factory=RealDictCursor)
            cursor = conn.cursor()
            print('DB connection success')
            break
    except Exception as error: 
            time.sleep(5)
            print('Error connecting to Db')
'''

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

@app.get("/sqlalchemy")
def test_pois(db: Session = Depends(get_db)):
    return {"status": "success"}


@app.get("/")
def root():
    return {"message": "Welcome to my Python API"}

