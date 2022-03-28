from typing import List

from fastapi import APIRouter, Depends, HTTPException, Response, status
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from .. import models, oauth2, schemas
from ..database import get_db

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter()

router = APIRouter(prefix="/pois", tags=["Comments"])


@router.get(
    "/comments/{id}", status_code=status.HTTP_200_OK, response_model=schemas.CommentOut
)
def get_comments(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    found_comments = db.query(models.Comment).filter(models.Comment.id == id)
    comment = found_comments.first()
    return comment


# Creates Comments associated with a given POI
@router.post(
    "/{id}/comments",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.CommentOut,
)
def create_comments(
    id: int,
    comment: schemas.Comment,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    new_comment = models.Comment(**comment.dict())
    new_comment.poi_id = id  # Takes POI Id from request
    new_comment.creator = current_user.id  # Sets Current User as creator
    db.add(new_comment)  # Adds to DB
    db.commit()  # Commits to DB
    db.refresh(new_comment)
    return new_comment  # Returns Comment


# Retrieves all comments associated with a given poi
@router.get(
    "/{poi_id}/comments",
    status_code=status.HTTP_200_OK,
    response_model=List[schemas.CommentOut],
)
def get_poi_comments(
    poi_id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    all_poi_comments = (
        db.query(models.Comment)
        .join(models.Poi, models.Poi.id == models.Comment.poi_id, isouter=True)
        .group_by(models.Comment.id)
        .filter(models.Poi.id == poi_id)
        .all()
    )
    print(all_poi_comments)
    return all_poi_comments


@router.put(
    "/{poi_id}/comments/{id}",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.CommentOut,
)
def update_comments(
    id: int,
    poi_id: int,
    comment: schemas.Comment,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    find_comment = db.query(models.Comment).filter(
        models.Comment.id == id
    )  # Keep query and first() filter on separate variables
    update_comment = find_comment.first()
    print(update_comment)
    if update_comment == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"poi with id: {id} does not exist",
        )
    # Update only own comments by logged in user
    if update_comment.creator != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Cannot Update Comment"
        )
    update_comment.creator = current_user.id
    find_comment.update(comment.dict(), synchronize_session=False)
    db.commit()
    return update_comment


# Allows user to delete own comments only
@router.delete("/{poi_id}/comments/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_poi(
    id: int,
    poi_id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    find_comment = db.query(models.Comment).filter(models.Comment.id == id)
    delete_comment = find_comment.first()
    print(delete_comment)
    if delete_comment == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"poi with id: {id} does not exist",
        )
    # delete only pois created by logged in user
    if find_comment.first().creator != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Cannot delete poi"
        )
    find_comment.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
