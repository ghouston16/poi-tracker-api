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
    prefix="/categories",
    tags=['Categories']
)
    # I am making a change
@router.get("",status_code=status.HTTP_200_OK, response_model=List[schemas.CategoryOut])
def get_categories(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    all_categories = db.query(models.Category).all()
   # print(all_categorys)
    return all_categories

@router.post("", status_code=status.HTTP_201_CREATED, response_model=schemas.CategoryOut)
def create_category(category: schemas.Category, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    new_category = models.Category(**category.dict())
    new_category.creator = current_user.id
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category

@router.get("/{id}/pois", status_code=status.HTTP_200_OK, response_model=List[schemas.Poi])
def get_category_pois(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    pois = db.query(models.Poi).filter(models.Poi.category== id).all()
    if not pois:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"category with id: {id} was not found")
    return pois

@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.CategoryOut)
def get_category(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    category = db.query(models.Category).filter(models.Category.id == id).first()
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"category with id: {id} was not found")
    return category

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    if current_user:
        find_category = db.query(models.Category).filter(models.Category.id == id)
        if find_category.first() == None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"category with id: {id} does not exist")
        # delete only categorys created by logged in user
        print(find_category)
        if find_category.first().creator != current_user.id:
                    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail=f"Cannot delete category")
        find_category.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}",status_code=status.HTTP_201_CREATED, response_model=schemas.CategoryOut)
def update_category(id: int, category: schemas.Category, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    find_category = db.query(models.Category).filter(models.Category.id == id)
    update_category = find_category.first()
    print(update_category)
    if update_category == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"category with id: {id} does not exist")
      # Update only categorys created by logged in user
    if update_category.creator != current_user.id:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Cannot delete category")
    update_category.creator = update_category.creator
    find_category.update(category.dict(), synchronize_session=False)
    db.commit()         
    return update_category
