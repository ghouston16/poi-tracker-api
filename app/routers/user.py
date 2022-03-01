from typing import List
from fastapi import Depends, FastAPI, Response, status, HTTPException, APIRouter
from pydantic import BaseModel
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db
from passlib.context import CryptContext

from app import database, oauth2


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter(
    prefix="/users",
    tags=['Users']
)

# User Methods

# Create user in DB with SQLAlchemy
@router.post("", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
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
@router.get("",status_code=status.HTTP_200_OK, response_model=List[schemas.UserOut])
def get_users(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    all_users = db.query(models.User).all()
    return all_users

# Get Individual User by Id
@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    find_user = db.query(models.User).filter(models.User.id == id)
    user = find_user.first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"poi with id: {id} was not found")

    #TO-DO: Remove this control
     # Check requested user against current user id - only allow matching ids
    #if user.id != current_user.id: 
    #           raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
    #                        detail=f"Cannot Access This User")
    return user

# Update user
@router.put("/{id}", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def update_user(id: int, updated_user: schemas.UserCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    find_user = db.query(models.User).filter(models.User.id == id)
    user = find_user.first()
    if user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user with id: {id} does not exist")
     # Check requested user against current user id - only allow matching ids
    if user.id != current_user.id:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Cannot Update This User")
    # To-do: hash the password - user.password
    hashed_pwd = pwd_context.hash(user.password)
    updated_user.password = hashed_pwd
    find_user.update(updated_user.dict(), synchronize_session=False)
    db.commit()
    return find_user.first()

# Delete user - Find by Id and Delete
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    user = db.query(models.User).filter(models.User.id == id)
    if user.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user with id: {id} does not exist")
    # Check requested user against current user id - only allow matching ids
    if user.first().id != current_user.id:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Cannot delete this user")
    user.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

