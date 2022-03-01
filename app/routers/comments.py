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


@router.post("/{id}/comments", status_code=status.HTTP_201_CREATED, response_model=schemas.CommentOut)
def create_comments(id: int, comment: schemas.Comment, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    new_comment = models.Comment(**comment.dict())
    new_comment.commented_poi = id
    new_comment.creator = current_user.id
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment
