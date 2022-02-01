import pytest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import get_db
from app.database import Base
import pytest
from app import models


SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:Expires21!!@localhost/poi_api_db_test'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture()
def client(session): # session param calls session fixture before code
# Create tables before code runs
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    #Base.metadata.drop_all(bind=engine) # Delete Tables after test

@pytest.fixture
def test_pois(client):
    pois_data = [{ "title": "title of poi 1", "description": "content of poi 1",
             "category": "Historic", "lat": "", "lng": "", "id": 1},{
            "title": "title of poi 2", "description": "content of poi 2", 
            "category": "Historic", "lat": "", "lng": "", "id": 2 }]
    test_poi1 = client.post("/pois", json=pois_data[0])
    assert test_poi1.status_code == 201
    test_poi2 = client.post("/pois", json=pois_data[1])
    assert test_poi2.status_code == 201

@pytest.fixture
def test_users(client):
    users_data = [{ "email": "test1@api.ie", "password": "secretword"} ,{ "email": "test2@api.ie", "password": "secretword"} ]
    test_user1 = client.post("/users", json=users_data[0])
    assert test_user1.status_code == 201
    test_user2 = client.post("/users", json=users_data[1])
    assert test_user2.status_code == 201
