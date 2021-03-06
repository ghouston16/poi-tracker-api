from typing import List

from fastapi import APIRouter, Depends, HTTPException, Response, status
from passlib.context import CryptContext
from sqlalchemy import func
from sqlalchemy.orm import Session

from .. import models, oauth2, schemas
from ..database import get_db

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter()

router = APIRouter(prefix="/pois", tags=["POIs"])
# Get all pois from the database
@router.get("", status_code=status.HTTP_200_OK, response_model=List[schemas.Poi])
def get_pois(
    db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)
):
    all_pois = db.query(models.Poi).all()
    # print(all_pois)
    return all_pois


# Create a new poi route
@router.post("", status_code=status.HTTP_201_CREATED, response_model=schemas.Poi)
def create_pois(
    poi: schemas.PoiCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    new_poi = models.Poi(**poi.dict())
    new_poi.creator = current_user.id
    db.add(new_poi)
    db.commit()
    db.refresh(new_poi)
    return new_poi


# Get likes by poi id
@router.get(
    "/{id}/likes", status_code=status.HTTP_200_OK, response_model=schemas.PoiOut
)
def get_poi_likes(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    poi = (
        db.query(models.Poi, func.count(models.Like.poi_id).label("likes"))
        .join(models.Like, models.Like.poi_id == models.Poi.id, isouter=True)
        .group_by(models.Poi.id)
        .filter(models.Poi.id == id)
        .first()
    )
    if not poi:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"poi with id: {id} was not found",
        )
    return poi


# Get a poi by id
@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.Poi)
def get_poi(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    poi = db.query(models.Poi).filter(models.Poi.id == id).first()
    if not poi:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"poi with id: {id} was not found",
        )
    return poi


# Delete a poi by id
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_poi(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    if current_user:
        find_poi = db.query(models.Poi).filter(models.Poi.id == id)
        if find_poi.first() == None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"poi with id: {id} does not exist",
            )
        # delete only pois created by logged in user
        print(find_poi)
        if find_poi.first().creator != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail=f"Cannot delete poi"
            )
        find_poi.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)


# Update a poi by id
@router.put("/{id}", status_code=status.HTTP_201_CREATED, response_model=schemas.Poi)
def update_poi(
    id: int,
    poi: schemas.PoiCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    find_poi = db.query(models.Poi).filter(models.Poi.id == id)
    update_poi = find_poi.first()
    print(update_poi)
    if update_poi == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"poi with id: {id} does not exist",
        )
    # Update only pois created by logged in user
    if update_poi.creator != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Cannot delete poi"
        )
    update_poi.creator = current_user.id
    find_poi.update(poi.dict(), synchronize_session=False)
    db.commit()
    return update_poi
