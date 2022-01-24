from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange

app = FastAPI()

id = 0
class Poi(BaseModel):
    title: str
    description: str
    category: str
    lat: str
    long: str
    published: bool = True
    rating: Optional[int] = None


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
            
@app.get("/")
def root():
    return {"message": "Welcome to my Python API"}


@app.get("/pois")
def get_pois():
    return {"data": my_pois}


@app.post("/pois", status_code=status.HTTP_201_CREATED)
def create_pois(poi: Poi):
    poi_dict = poi.dict()
    global id 
    id += 1
    poi_dict['id'] = id
    my_pois.append(poi_dict)
    return {"data": poi_dict}


@app.get("/pois/{id}",  status_code=status.HTTP_200_OK)
def get_poi(id: int):

    poi = find_poi(id)
    if not poi:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"poi with id: {id} was not found")
    return {"poi_detail": poi}


@app.delete("/pois/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_poi(id: int):
    index = find_index_poi(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"poi with id: {id} does not exist")
    my_pois.pop(index)
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