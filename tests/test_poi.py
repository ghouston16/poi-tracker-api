from fastapi.testclient import TestClient
from app.main import app
import pytest

# Test Client Instance
@pytest.fixture()
def client(): 
    yield TestClient(app)

# Fixture Data for Testing
@pytest.fixture()
def test_pois():
    poi_data = [{"title": "title of poi 1", "description": "content of poi 1", "category": "Historic", "lat": "", "long": "", "id": 1,
            "title": "title of poi 2", "description": "content of poi 2", "category": "Historic", "lat": "", "long": "", "id": 2 }]

# Test for get All pois route
def test_get_all_pois(client, test_pois):
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
def test_get_poi_by_id(client):
    response = client.get("/pois/1")
    print(response.json())
    assert response.status_code == 200

# Test Delete POI 
def test_delete_poi(client):
    response = client.delete("/pois/1")
    assert response.status_code == 204

# Test Update POI
def test_update_poi(client):
    poi_data = {"title": "title of poi 3", "description": "content of poi 3", "category": "Historic", "lat": "1.000", "long": "4.000", "id": 1 }
    response = client.put("/pois/2",json= poi_data)
    assert response.status_code == 201
