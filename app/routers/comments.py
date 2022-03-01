from typing import List, Optional
from fastapi import Depends, FastAPI, Response, status, HTTPException, APIRouter
from sqlalchemy import func
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from ..database import get_db
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter()

router = APIRouter(
    prefix="/pois",
    tags=['Commnets']
)

    
@router.get("/comments",status_code=status.HTTP_200_OK, response_model=List[schemas.CommentOut])
def get_comments(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    all_comments = db.query(models.Comment).all()
    print(all_comments)
    return all_comments

# Creates Comments associated with a given POI
@router.post("/{id}/comments", status_code=status.HTTP_201_CREATED, response_model=schemas.CommentOut)
def create_comments(id: int, comment: schemas.Comment, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    new_comment = models.Comment(**comment.dict())
    new_comment.poi_id = id # Takes POI Id from request
    new_comment.creator = current_user.id # Sets Current User as creator
    db.add(new_comment) # Adds to DB
    db.commit() # Commits to DB 
    db.refresh(new_comment)
    return new_comment # Returns Comment

# Retrieves all comments associated with a given poi
@router.get("/{poi_id}/comments",status_code=status.HTTP_200_OK, response_model=List[schemas.CommentOut])
def get_comments(poi_id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    all_poi_comments = db.query(models.Comment).join(models.Poi,models.Poi.id==models.Comment.poi_id, isouter=True).group_by(models.Comment.id).filter(models.Poi.id == poi_id).all()
    print(all_poi_comments)
    return all_poi_comments

@router.put("/{poi_id}/comments/{id}", status_code=status.HTTP_201_CREATED, response_model=schemas.CommentOut)
def update_comments(id: int, poi_id: int, comment: schemas.Comment, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    find_comment = db.query(models.Comment).filter(models.Comment.id == id) # Keep query and first() filter on separate variables
    update_comment = find_comment.first()
    print(update_comment)
    if update_comment == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"poi with id: {id} does not exist")
      # Update only own comments by logged in user
    if update_comment.creator != current_user.id:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Cannot Update Comment")
    update_comment.creator = current_user.id
    find_comment.update(comment.dict(), synchronize_session=False)
    db.commit()         
    return update_comment
