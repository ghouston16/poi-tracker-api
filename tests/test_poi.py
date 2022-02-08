from fastapi.testclient import TestClient
from app.main import app
import pytest

# Test for get All pois route - Authenticated User
def test_authorized_get_all_posts(client_auth, test_posts):
    response = client_auth.get(
        "/posts")
    print(response.json())
    assert response.status_code == 200
    assert len(response.json()) == len(test_posts)

# Test for get All pois route unauthenticated
def test_no_auth_get_all_pois(client):
    response = client.get(
        "/pois")
    print(response.json())
    assert response.status_code == 403

# Test for Creating POI
def test_create_poi_auth(client_auth):
    poi_data = {"title": "title of poi 3", "description": "content of poi 3", "category": "Historic", "lat": "1.000", "lng": "4.000" }
    response = client_auth.post("/pois", json=poi_data)
    print(response.json())
    assert response.status_code == 201


# Test for unauthenticated attempt to create POI 
def test_create_poi_no_auth(client):
    poi_data = {"title": "title of poi 3", "description": "content of poi 3", "category": "Historic", "lat": "1.000", "lng": "4.000" }
    response = client.post("/pois", json=poi_data)
    print(response.json())
    assert response.status_code == 403

# Test for Find By Id
def test_get_poi_by_id(client, test_pois):
    response = client.get("/pois/1")
    print(response.json())
    assert response.status_code == 200

# Test Update POI
def test_update_poi(client, test_pois):
    poi_data = {"title": "updated", "description": "content of poi 3", "category": "Historic", "lat": "1.000", "lng": "4.000", "id": 1 }
    response = client.put("/pois/1",json= poi_data)
    assert response.status_code == 201

# Test Update POI
def test_update_poi(client_auth, test_pois):
    poi_data = {"title": "updated", "description": "content of poi 3", "category": "Historic", "lat": "1.000", "lng": "4.000", "id": 1 }
    response = client_auth.put("/pois/1",json= poi_data)
    assert response.status_code == 201


# Test Delete POI - No Atuh
def test_delete_poi(client, test_pois):
    response = client.delete("/pois/1")
    assert response.status_code == 403

# Test Authenticated User Delete POI 
def test_delete_poi(client_auth, test_pois):
    response = client_auth.delete("/pois/1")
    assert response.status_code == 204

