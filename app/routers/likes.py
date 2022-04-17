from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import database

from .. import models, oauth2, schemas

router = APIRouter(prefix="/like", tags=["Like"])

# Like a post
@router.post("/", status_code=status.HTTP_201_CREATED)
def like(
    like: schemas.Like,
    db: Session = Depends(database.get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    poi = db.query(models.Poi).filter(models.Poi.id == like.poi_id).first()
    if not poi:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Poi id: {like.poi_id} doe snot exist",
        )
    like_query = db.query(models.Like).filter(
        models.Like.poi_id == like.poi_id, models.Like.user_id == current_user.id
    )
    # Cannot like same post twice
    found_like = like_query.first()
    if like.dir == 1:
        if found_like:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"user {current_user.id} has already liked on this poi",
            )
        new_like = models.Like(poi_id=like.poi_id, user_id=current_user.id)
        db.add(new_like)
        db.commit()
        return {"message": "successfully added like"}
    else:
        if not found_like:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Like does not Exist"
            )

        like_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "Like Removed"}
