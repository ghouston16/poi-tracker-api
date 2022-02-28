from random import randint
from fastapi.testclient import TestClient
from app.main import app
from app import schemas
import pytest

# Test for unauthenticated attempt to create POI 
def test_create_poi_no_auth(client):
    poi_data = {"title": "title of poi 3", "description": "content of poi 3", "category": "Historic", "lat": "1.000", "lng": "4.000" }
    response = client.post("/pois", json=poi_data)
    print(response.json())
    assert response.status_code == 401

# Test for get All pois route unauthenticated
def test_no_auth_get_all_pois(client):
    response = client.get(
        "/pois")
    print(response.json())
    assert response.status_code == 401

# Test for Find By Id - No Auth User
def test_get_poi_by_id_no_auth(client):
   response = client.get(
       f"/pois/1")
   print(response.json())
   assert response.status_code == 401


# Test Update POI - No Auth
def test_update_poi_no_auth(client):
    poi_data = {"title": "updated", "description": "content of poi 3", "category": "Historic", "lat": "1.000", "lng": "4.000", "id": 1, "creator": 1 }
    response = client.put("/pois/1",json= poi_data)
    assert response.status_code == 401

# Test for get All pois route - Authenticated User
def test_authorized_get_all_pois(client_auth, test_pois):
    response = client_auth.get(
        "/pois")
    print(response.json())
    print(test_pois)
    assert response.status_code == 200
    # assert len(response.json()) == len(test_pois)

# Test for Creating POI
def test_create_poi_auth(client_auth, test_user):
    poi_data = {"title": "title of poi 3", "description": "poi 3", "category": "Historic", "lat": "1.000", "lng": "4.000", "published": True, "creator": test_user['id'] }
    response = client_auth.post("/pois", json=poi_data)
    created_poi = schemas.Poi(**response.json())
    assert response.status_code == 201
    assert created_poi.title == "title of poi 3"
    assert created_poi.description == "poi 3"
    assert created_poi.id == test_user['id']
    assert created_poi.published == True


# Test for Find By Id - Auth User
def test_get_poi_by_id(client_auth, test_pois):
    response = client_auth.get(
        f"/pois/1")
    found_poi = schemas.PoiOut(**response.json())
    test_poi = test_pois[0]
    assert found_poi.Poi.title == test_poi['title']
    assert response.status_code == 200

    
# Test Update POI - Auth
def test_update_poi(client_auth, test_pois, test_user):
    poi_data = {"title": "updated", "description": "content of poi 3", "category": "Historic", "lat": "1.000", "lng": "4.000", "id": 1, "creator": test_user['id'] }
    response = client_auth.put("/pois/1",json= poi_data)
    updated_poi = schemas.Poi(**response.json())
    assert response.status_code == 201
    assert updated_poi.title == poi_data['title']
    assert updated_poi.description == poi_data['description']
    assert updated_poi.category == poi_data['category']
    assert updated_poi.lat == poi_data['lat']
    assert updated_poi.lng == poi_data['lng']
    assert updated_poi.creator == poi_data['creator']


# Test Delete POI - No Atuh
def test_delete_poi(client, test_pois):
    response = client.delete("/pois/1")
    assert response.status_code == 401

# Test Authenticated User Delete POI 
def test_delete_poi(client_auth, test_pois):
    response = client_auth.delete("/pois/1")
    assert response.status_code == 204

