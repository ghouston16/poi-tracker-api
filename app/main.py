from operator import mod
from typing import List, Optional
from fastapi import Depends, FastAPI, Response, status, HTTPException
from fastapi.params import Body
from importlib_metadata import re
from itsdangerous import TimedSerializer
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models, schemas
from .database import engine, get_db

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

class Poi(BaseModel):
    title: str
    description: str
    category: str
    lat: str
    long: str
    published: bool = True
    

while True:
    try:
            conn = psycopg2.connect(host='localhost', database='poi_api_db',user='postgres',password='Expires21!!', cursor_factory=RealDictCursor)
            cursor = conn.cursor()
            print('DB connection success')
            break
    except Exception as error: 
            TimedSerializer.sleep(5)
            print('Error connecting to Db')

my_pois = [{"title": "title of poi 1", "description": "content of poi 1",
             "category": "Historic", "lat": "", "long": "", "id": 1,
            "title": "title of poi 2", "description": "content of poi 2", 
            "category": "Historic", "lat": "", "long": "", "id": 2 }]

@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    return {"status": "success"}


@app.get("/")
def root():
    return {"message": "Welcome to my Python API"}


@app.get("/pois",status_code=status.HTTP_200_OK, response_model=List[schemas.Poi])
def get_pois(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM pois""")
    # pois = cursor.fetchall()
    pois = db.query(models.Poi).all()
    return pois


@app.post("/pois", status_code=status.HTTP_201_CREATED, response_model=schemas.Poi)
def create_pois(poi: Poi, db: Session = Depends(get_db)):
    #cursor.execute("""INSERT INTO pois (title,description,category,lat,long,published) values (%s,%s,%s,%s,%s,%s)""",(poi.title,poi.description,poi.category,poi.lat,poi.long,poi.published))
    new_poi = models.Poi(**poi.dict())
    db.add(new_poi)
    db.commit()
    db.refresh(new_poi)
    return new_poi


@app.get("/pois/{id}", status_code=status.HTTP_200_OK, response_model=schemas.Poi)
def get_poi(id: int, db: Session = Depends(get_db)):
    find_poi = db.query(models.Poi).filter(models.Poi.id == id)
    #cursor.execute("""SELECT FROM pois WHERE id = %s""", (str(id),) )
    # poi = cursor.fetchone()
    poi = find_poi.first()
    if not poi:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"poi with id: {id} was not found")
    return poi


@app.delete("/pois/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_poi(id: int, db: Session = Depends(get_db)):
    find_poi = db.query(models.Poi).filter(models.Poi.id == id)
    
    #cursor.execute("""DELETE FROM pois WHERE id = %s""", (str(id),) )
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