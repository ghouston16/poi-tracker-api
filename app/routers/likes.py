from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional
from .. import models, schemas, oauth2
from ..database import get_db
from app import database


router = APIRouter(
    prefix="/like",
    tags=['Like']
)
@router.post("/", status_code=status.HTTP_201_CREATED)
def like(like: schemas.Like, db: Session = Depends(database.get_db), 
current_user: int =Depends(oauth2.get_current_user)):
    poi = db.query(models.Poi).filter(models.Poi.id== like.poi_id).first()
    if not poi:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Poi id: {like.poi_id} doe snot exist")
    like_query = db.query(models.Like).filter(models.Like.poi_id == like.poi_id, models.Like.user_id== current_user.id)
    found_like = like_query.first()
    if (like.dir == 1): 
        if found_like: 
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
            detail= f"user {current_user.id} has already liked on this poi")
        new_like = models.Like(poi_id= like.poi_id, user_id=current_user.id)
        db.add(new_like)
        db.commit()
        return {"message": "successfully added like"}
    else:
        if not found_like:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Like does not Exist")
        
        like_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "Like Removed"}
