import py
import pytest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import get_db
from app.database import Base
import pytest
from app import models
from app.oauth2 import create_access_token
from app.config import settings

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Creates a connection to testing DB and ensures tables are correct
@pytest.fixture()
def session():
    # Drop all drops in testing DB
    Base.metadata.drop_all(bind=engine)
    # Create tables fresh
    Base.metadata.create_all(bind=engine)
    # Create session
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
    

# Fixture for creating testing jwt
@pytest.fixture()
def access_token(test_user):
    return create_access_token({"user_id":test_user['id']})

@pytest.fixture()
def client_auth(client, access_token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {access_token}"
    }
    return client

# Test POI fixture data for pytest

@pytest.fixture
def test_pois(client_auth):
    pois_data = [{ "id": 1, "title": "title of poi 1", "description": "words about a place",
             "category": "Historic", "lat": "", "lng": "", "creator": 1},{
            "title": "title of poi 2", "description": "content of poi 2", 
            "category": "Historic", "lat": "", "lng": "", "id": 2, "creator": 1}]
    test_poi1 = client_auth.post("/pois", json=pois_data[0])
    assert test_poi1.status_code == 201
    test_poi2 = client_auth.post("/pois", json=pois_data[1])
    assert test_poi2.status_code == 201
    response = client_auth.get("/pois")

    new_pois = response.json()
    print(new_pois)
    return new_pois

@pytest.fixture
def test_users(client):
    users_data = [{ "id": 1,"email": "test1@api.ie", "password": "secretword"} ,{ "id": 2,"email": "test2@api.ie", "password": "secretword"} ]
    test_user1 = client.post("/users", json=users_data[0])
    assert test_user1.status_code == 201
    test_user2 = client.post("/users", json=users_data[1])
    assert test_user2.status_code == 201
    return users_data 

# Test User fixture
@pytest.fixture
def test_user(client):
    users_data = { "email": "test3@api.ie", 
                    "password": "secretword" 
                }
    response = client.post("/users", json=users_data)
    assert response.status_code == 201
    print(response)
    new_user = (response.json())
    assert new_user['email'] == users_data["email"]
    new_user['password'] = users_data['password']
    return new_user


# Second Test User
@pytest.fixture()
def test_user2(client):
    user_data = {
        "email": "g@gmail.com",
        "password": "password123"
    }
    response = client.post("/users", json=user_data)
    assert response.status_code == 201
    print(response)
    new_user = (response.json())
    assert new_user['email'] == user_data["email"]
    new_user['password'] = user_data['password']
    return new_user
