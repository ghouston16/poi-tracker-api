from ast import List
from random import randint
from fastapi.testclient import TestClient
from app.main import app
from app import schemas
import pytest


# Test for unauthenticated attempt to category on a poi
def test_create_category_no_auth(client):
    category_data = {"name": "category 3", "creator": 1}
    response = client.post(f"/categories", json=category_data)
    print(response.json())
    assert response.status_code == 401  # Unauthorized


# Test for get All categories route unauthenticated
def test_no_auth_get_all_poi_categories(client):
    response = client.get(f"/categories")
    print(response.json())
    assert response.status_code == 401  # Unauthorized


# Test for category Find By Id - No Auth User
def test_get_category_by_id_no_auth(client):
    response = client.get(f"/categories/1")
    print(response.json())
    assert response.status_code == 401  # Unauthorized


# Test Update category - No Auth
def test_update_category_no_auth(client):
    category_data = {"name": "updated", "creator": 1}
    response = client.put(f"/categories/1", json=category_data)
    assert response.status_code == 401  # Unauthorized


# Test for Creating POI Category
def test_create_category_auth(client_auth, test_user, test_categories):
    category_data = {"name": "test", "creator": test_user["id"]}
    response = client_auth.post(f"/categories", json=category_data)
    created_category = schemas.CategoryOut(**response.json())
    assert response.status_code == 201  # Content Created
    assert created_category.name == category_data["name"]
    assert created_category.creator == test_user["id"]


# Test for Find By Id - Auth User
# def test_get_pois_by_category(client_auth, test_categories, test_pois):
# response = client_auth.get(
#    f"/categories/{test_categories[0]}/pois")
# found_pois = response.json()
# pois = found_pois.dict()
# print(pois)
# pois = [schemas.Poi(**found_pois)]
# test_poi = schemas.Poi(**pois[0])
# assert test_categories== pois[0].id
# assert response.status_code == 200

# Test Update POI - Auth
def test_update_category_auth(client_auth, test_categories, test_user):
    category_data = {"name": "test category", "creator": test_user["id"]}
    response = client_auth.put(
        f"/categories/{test_categories[0]['id']}", json=category_data
    )
    updated_category = schemas.CategoryOut(**response.json())
    assert response.status_code == 201  # Category Update Created
    assert updated_category.name == category_data["name"]
    assert updated_category.creator == category_data["creator"]


# Test Delete POI - No Atuh
def test_delete_category(client):
    response = client.delete(f"/categories/1")
    assert response.status_code == 401  # Unauthorized


# Test Authenticated User Delete POI
def test_delete_category_auth(client_auth, test_categories, test_user):
    response = client_auth.delete(f"/categories/{test_categories[0]['id']}")
    assert response.status_code == 204  # No Content Found
