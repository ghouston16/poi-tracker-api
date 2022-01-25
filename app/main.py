
from typing import Optional
from fastapi import Depends, FastAPI, Response, status, HTTPException
from fastapi.params import Body
from itsdangerous import TimedSerializer
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models
from .database import engine, get_db

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

id = 0
class Poi(BaseModel):
    title: str
    description: str
    category: str
    lat: str
    long: str
    published: bool = True
    rating: Optional[int] = None

while True:
    try:
            conn = psycopg2.connect(host='localhost', database='poi_api_db',user='postgres',password='Expires21!!', cursor_factory=RealDictCursor)
            cursor = conn.cursor()
            print('DB connection success')
            break
    except Exception as error: 
            TimedSerializer.sleep(5)
            print('Error connecting to Db')

my_pois = [{"title": "title of poi 1", "description": "content of poi 1", "category": "Historic", "lat": "", "long": "", "id": 1,
            "title": "title of poi 2", "description": "content of poi 2", "category": "Historic", "lat": "", "long": "", "id": 2 }]


def find_poi(id):
    for p in my_pois:
        if p['id'] == id:
            return p


def find_index_poi(id):
    for i, p in enumerate(my_pois):
        if p['id'] == id:
            return i

@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    return {"status": "success"}


@app.get("/")
def root():
    return {"message": "Welcome to my Python API"}


@app.get("/pois", status_code=status.HTTP_200_OK)
def get_pois():
    cursor.execute("""SELECT * FROM pois""")
    pois = cursor.fetchall()
    return {"data": pois}


@app.post("/pois", status_code=status.HTTP_201_CREATED)
def create_pois(poi: Poi):
    global id 
    id +=1
    cursor.execute("""INSERT INTO pois (title,description,category,lat,long,published,id) values (%s,%s,%s,%s,%s,%s,%s)""",(poi.title,poi.description,poi.category,poi.lat,poi.long,poi.published,id))
    conn.commit()
    return {"data": "new poi created"}


@app.get("/pois/{id}",  status_code=status.HTTP_200_OK)
def get_poi(id: int):
    cursor.execute("""SELECT FROM pois WHERE id = %s""", (str(id),) )
    poi = cursor.fetchone()
    if not poi:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"poi with id: {id} was not found")
    return {"poi_detail": poi}


@app.delete("/pois/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_poi(id: int):
    cursor.execute("""DELETE FROM pois WHERE id = %s""", (str(id),) )
    found_poi = cursor.fetchone()
    if found_poi == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"poi with id: {id} does not exist")
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/pois/{id}",status_code=status.HTTP_201_CREATED)
def update_poi(id: int, poi: Poi):
    index = find_index_poi(id)

    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"poi with id: {id} does not exist")

    poi_dict = poi.dict()
    poi_dict['id'] = id
    my_pois[index] = poi_dict
    return {"data": poi_dict}