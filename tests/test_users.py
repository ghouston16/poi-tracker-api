from fastapi.testclient import TestClient
from app.main import app
import pytest
from jose import jwt
from app import schemas
from app.config import settings

# Test for get All users route
def test_get_all_users(client_auth):
    response = client_auth.get(
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
def test_get_user_by_id(client_auth, test_users):
    response = client_auth.get("/users/1")
    print(response.json())
    assert response.status_code == 200

# Test Update User
def test_update_user(client_auth, test_users):
    user_data = {"email": "changed@email.ie", 
                "password": "secretworld" }
    response = client_auth.put("/users/1",json= user_data)
    assert response.status_code == 201

# Test Delete User 
def test_delete_user(client_auth, test_user):
    response = client_auth.delete(f"/users/{test_user['id']}")
    print(response)
    assert response.status_code == 204

# Test User Login
def test_login_user(client, test_user2):
    res = client.post(
        "/login", data={"username": test_user2["email"], 
        "password": test_user2["password"]})
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token,settings.secret_key, algorithms=[settings.algorithm])
    id: str = payload.get("user_id")
    assert id == test_user2['id']
    assert login_res.token_type == "bearer"
    assert res.status_code == 200

# Test Different Types of Incorrect Login using Parametrize
@pytest.mark.parametrize("email, password, status_code", [("wrong@email.com","wrong",403), ("thisiswrong@mail.com","wrongagain",403),(None, "password",422)])
def test_incorrect_login(client, test_user2, email,password,status_code):
    res = client.post(
        "/login", data={"username": email, 
        "password": password})
    assert res.status_code == status_code
