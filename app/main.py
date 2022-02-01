from enum import auto
from operator import mod
from typing import List, Optional
from fastapi import Depends, FastAPI, Response, status, HTTPException
from fastapi.params import Body
from itsdangerous import TimedSerializer
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from pytest import deprecated_call
from sqlalchemy.orm import Session

from app.config import settings
from . import models, schemas
from .database import engine, get_db
from passlib.context import CryptContext

from app import database

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

class Poi(BaseModel):
    title: str
    description: str
    category: str
    lat: str
    lng: str
    published: bool = True
    

while True:
    try:
            conn = psycopg2.connect(host=settings.database_hostname, database=settings.database_name,user=settings.database_username,password=settings.database_password, cursor_factory=RealDictCursor)
            cursor = conn.cursor()
            print('DB connection success')
            break
    except Exception as error: 
            time.sleep(5)
            print('Error connecting to Db')


@app.get("/sqlalchemy")
def test_pois(db: Session = Depends(get_db)):
    return {"status": "success"}


@app.get("/")
def root():
    return {"message": "Welcome to my Python API"}


@app.get("/pois",status_code=status.HTTP_200_OK, response_model=List[schemas.Poi])
def get_pois(db: Session = Depends(get_db)):
    all_pois = db.query(models.Poi).all()
    return all_pois


@app.post("/pois", status_code=status.HTTP_201_CREATED, response_model=schemas.Poi)
def create_pois(poi: Poi, db: Session = Depends(get_db)):
    new_poi = models.Poi(**poi.dict())
    db.add(new_poi)
    db.commit()
    db.refresh(new_poi)
    return new_poi


@app.get("/pois/{id}", status_code=status.HTTP_200_OK, response_model=schemas.Poi)
def get_poi(id: int, db: Session = Depends(get_db)):
    find_poi = db.query(models.Poi).filter(models.Poi.id == id)
    poi = find_poi.first()
    if not poi:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"poi with id: {id} was not found")
    return poi


@app.delete("/pois/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_poi(id: int, db: Session = Depends(get_db)):
    find_poi = db.query(models.Poi).filter(models.Poi.id == id)
    if find_poi.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"poi with id: {id} does not exist")
    find_poi.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/pois/{id}",status_code=status.HTTP_201_CREATED, response_model=schemas.Poi)
def update_poi(id: int, poi: schemas.PoiCreate, db: Session = Depends(get_db)):
    find_poi = db.query(models.Poi).filter(models.Poi.id == id)
    update_poi = find_poi.first()
    if update_poi == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"poi with id: {id} does not exist")

    find_poi.update(poi.dict(), synchronize_session=False)
    db.commit()         
    return update_poi

# User Methods

# Create user in DB with SQLAlchemy
@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # TO-DO :hash the password - user.password
    hashed_pwd = pwd_context.hash(user.password)
    user.password = hashed_pwd
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# Retrieve all users from DB and return List/Array
@app.get("/users",status_code=status.HTTP_200_OK, response_model=List[schemas.UserOut])
def get_users(db: Session = Depends(get_db)):
    all_users = db.query(models.User).all()
    return all_users

# Get Individual User by Id
@app.get("/users/{id}", status_code=status.HTTP_200_OK, response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    find_user = db.query(models.User).filter(models.User.id == id)
    user = find_user.first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"poi with id: {id} was not found")
    return user

# Update user
@app.put("/users/{id}", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def update_user(id: int, updated_user: schemas.UserCreate, db: Session = Depends(get_db)):
    find_user = db.query(models.User).filter(models.User.id == id)
    user = find_user.first()
    if user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user with id: {id} does not exist")
    # To-do: hash the password - user.password
    find_user.update(updated_user.dict(), synchronize_session=False)
    db.commit()
    return find_user.first()

# Delete user - Find by Id and Delete
@app.delete("/users/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id)
    if user.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user with id: {id} does not exist")
    user.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

