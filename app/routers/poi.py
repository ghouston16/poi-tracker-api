from typing import List, Optional
from fastapi import Depends, FastAPI, Response, status, HTTPException, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter()

router = APIRouter(
    prefix="/pois",
    tags=['POIs']
)

    
@router.get("",status_code=status.HTTP_200_OK, response_model=List[schemas.Poi])
def get_pois(db: Session = Depends(get_db)):
    all_pois = db.query(models.Poi).all()
    return all_pois


@router.post("", status_code=status.HTTP_201_CREATED, response_model=schemas.Poi)
def create_pois(poi: schemas.PoiCreate, db: Session = Depends(get_db)):
    new_poi = models.Poi(**poi.dict())
    db.add(new_poi)
    db.commit()
    db.refresh(new_poi)
    return new_poi


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.Poi)
def get_poi(id: int, db: Session = Depends(get_db)):
    find_poi = db.query(models.Poi).filter(models.Poi.id == id)
    poi = find_poi.first()
    if not poi:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"poi with id: {id} was not found")
    return poi


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_poi(id: int, db: Session = Depends(get_db)):
    find_poi = db.query(models.Poi).filter(models.Poi.id == id)
    if find_poi.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"poi with id: {id} does not exist")
    find_poi.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}",status_code=status.HTTP_201_CREATED, response_model=schemas.Poi)
def update_poi(id: int, poi: schemas.PoiCreate, db: Session = Depends(get_db)):
    find_poi = db.query(models.Poi).filter(models.Poi.id == id)
    update_poi = find_poi.first()
    if update_poi == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"poi with id: {id} does not exist")

    find_poi.update(poi.dict(), synchronize_session=False)
    db.commit()         
    return update_poi
