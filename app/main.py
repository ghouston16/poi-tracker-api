from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from .database import get_db
from .routers import authenticate, categories, comments, likes, poi, user

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Create Api instance
app = FastAPI()

# Obselete with Alembic Migrations
# models.Base.metadata.create_all(bind=engine)

# Change this to Web App URL
origins = ["*"]

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(poi.router)
app.include_router(user.router)
app.include_router(authenticate.router)
app.include_router(likes.router)
app.include_router(comments.router)
app.include_router(categories.router)


@app.get("/sqlalchemy")
def test_pois(db: Session = Depends(get_db)):
    return {"status": "success"}


@app.get("/")
def root():
    return {"message": "Welcome to my Python API - demo changes"}
