from unicodedata import category
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
from app import models, schemas
from app.oauth2 import create_access_token
from app.config import settings

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"

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
def client(session):  # session param calls session fixture before code
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
    return create_access_token({"user_id": test_user["id"]})


@pytest.fixture()
def client_auth(client, access_token):
    client.headers = {**client.headers, "Authorization": f"Bearer {access_token}"}
    return client


# Test POI fixture data for pytest
@pytest.fixture
def test_pois(client_auth):  # Authorized client needed to create
    pois_data = [
        {
            "id": 1,
            "title": "title of poi 1",
            "description": "words about a place",
            "category": 1,
            "lat": "",
            "lng": "",
            "creator": 1,
        },
        {
            "title": "title of poi 2",
            "description": "content of poi 2",
            "category": 2,
            "lat": "",
            "lng": "",
            "id": 2,
            "creator": 1,
        },
    ]
    test_poi1 = client_auth.post("/pois", json=pois_data[0])
    assert test_poi1.status_code == 201
    test_poi2 = client_auth.post("/pois", json=pois_data[1])
    assert test_poi2.status_code == 201
    response = client_auth.get("/pois")
    new_pois = response.json()
    print(new_pois)
    return new_pois


# Users fixtures for testing purposes
@pytest.fixture
def test_users(client):
    users_data = [
        {"id": 1, "email": "test1@api.ie", "password": "secretword"},
        {"id": 2, "email": "test2@api.ie", "password": "secretword"},
    ]
    test_user1 = client.post("/users", json=users_data[0])
    assert test_user1.status_code == 201
    test_user2 = client.post("/users", json=users_data[1])
    assert test_user2.status_code == 201
    return users_data


# Test User fixture for testing
@pytest.fixture
def test_user(client):
    users_data = {"email": "test3@api.ie", "password": "secretword"}
    response = client.post("/users", json=users_data)
    assert response.status_code == 201
    print(response)
    new_user = response.json()
    assert new_user["email"] == users_data["email"]
    new_user["password"] = users_data["password"]
    return new_user


# Second Test User fixtures for testing purposes
@pytest.fixture()
def test_user2(client):
    user_data = {"email": "g@gmail.com", "password": "password123"}
    response = client.post("/users", json=user_data)
    assert response.status_code == 201
    print(response)
    new_user = response.json()
    assert new_user["email"] == user_data["email"]
    new_user["password"] = user_data["password"]
    return new_user


# Comment fixtures for testing purposes
@pytest.fixture()
def test_comments(
    client_auth, test_user, test_pois
):  #  Authorized client needed to create
    comments_data = [
        {
            "comment": "test comment",
            "poi_id": test_pois[0]["id"],
            "creator": test_user["id"],
            "id": 1,
            "created_at": "2022-03-01T13:40:14.440465+00:00",
        },
        {
            "comment": "test comment",
            "poi_id": test_pois[0]["id"],
            "creator": test_user["id"],
            "id": 2,
            "created_at": "2022-03-01T13:41:02.889841+00:00",
        },
    ]
    response = client_auth.post(f"/pois/1/comments", json=comments_data[0])
    assert response.status_code == 201
    print(response)
    new_comment1 = response.json()
    assert new_comment1["comment"] == comments_data[0]["comment"]
    response = client_auth.post(f"/pois/2/comments", json=comments_data[1])
    assert response.status_code == 201
    new_comment2 = response.json()
    assert new_comment1["comment"] == comments_data[1]["comment"]
    test_comments = [new_comment1, new_comment2]
    # response2 = client_auth.get("/categories")
    # test_comments = response2.json()
    return test_comments


@pytest.fixture()
def test_categories(
    client_auth, test_user, test_pois
):  #  Authorized client needed to create
    categories_data = [
        {"name": "North", "creator": test_user["id"]},
        {
            "name": "South",
            "creator": test_user["id"],
        },
    ]

    response = client_auth.post("/categories", json=categories_data[0])
    assert response.status_code == 201
    print(response)
    new_category1 = response.json()
    assert new_category1["name"] == categories_data[0]["name"]
    response = client_auth.post("/categories", json=categories_data[1])
    assert response.status_code == 201
    new_category2 = response.json()
    assert new_category2["name"] == categories_data[1]["name"]
    test_categories = [new_category1, new_category2]
    return test_categories
