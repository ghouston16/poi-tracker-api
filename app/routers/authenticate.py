from app import models, oauth2, utils
from fastapi import (APIRouter, Depends, FastAPI, HTTPException, Response,
                     status)
from pytest import raises
from sqlalchemy.orm import Session

from .. import database, schemas
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(tags=['Authenication'])

@router.post('/login', response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    # Query DB for user by Email from login
    user = db.query(models.User).filter(
        models.User.email == user_credentials.username).first()
    # User not found
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Login")
    # Utils check() function will chekc against hashed pwd
    if not utils.check(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Login")
    # create JWT
    access_token = oauth2.create_jwt(data={"user_id": user.id})
    
    # Return JWT
    return {"access_token": access_token, "token_type": "bearer"}
    