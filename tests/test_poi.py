from fastapi.testclient import TestClient
from app.main import app
import pytest

# Test for get All pois route
def test_get_all_pois(client):
    response = client.get(
        "/pois")
    print(response.json())
    assert response.status_code == 200

# Test for Creating POI
def test_create_poi(client):
    poi_data = {"title": "title of poi 3", "description": "content of poi 3", "category": "Historic", "lat": "1.000", "long": "4.000" }
    response = client.post("/pois", json=poi_data)
    print(response.json())
    assert response.status_code == 201

# Test for Find By Id
def test_get_poi_by_id(client, test_pois):
    response = client.get("/pois/1")
    print(response.json())
    assert response.status_code == 200

# Test Update POI
def test_update_poi(client, test_pois):
    poi_data = {"title": "updated", "description": "content of poi 3", "category": "Historic", "lat": "1.000", "long": "4.000", "id": 1 }
    response = client.put("/pois/1",json= poi_data)
    assert response.status_code == 201

# Test Delete POI 
def test_delete_poi(client, test_pois):
    response = client.delete("/pois/1")
    assert response.status_code == 204

