from fastapi.testclient import TestClient
from app.main import app
import pytest

# Test for get All users route
def test_get_all_users(client):
    response = client.get(
        "/users")
    print(response.json())
    assert response.status_code == 200

# Test for Creating User
def test_create_user(client):
    user_data = {"email": "test@test.com", "password": "Password123" }
    response = client.post("/users", json=user_data)
    print(response.json())
    assert response.status_code == 201

# Test for Find By Id
def test_get_user_by_id(client, test_users):
    response = client.get("/users/1")
    print(response.json())
    assert response.status_code == 200

# Test Update User
def test_update_user(client, test_users):
    user_data = {"email": "changed@email.ie", 
                "password": "secretworld" }
    response = client.put("/users/1",json= user_data)
    assert response.status_code == 201

# Test Delete User 
def test_delete_user(client, test_users):
    response = client.delete("/users/1")
    assert response.status_code == 204

