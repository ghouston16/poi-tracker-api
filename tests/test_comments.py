from random import randint
from fastapi.testclient import TestClient
from app.main import app
from app import schemas
import pytest


# Test for unauthenticated attempt to create POI 
def test_create_comment_no_auth(client):
    comment_data = {"comment": "comment 3", "creator": 1, "commented_poi": 1, "published": True }
    response = client.post("/comments", json=comment_data)
    print(response.json())
    assert response.status_code == 401

# Test for get All comments route unauthenticated
def test_no_auth_get_all_comments(client):
    response = client.get(
        "/comments")
    print(response.json())
    assert response.status_code == 401

# Test for Find By Id - No Auth User
def test_get_comment_by_id_no_auth(client):
   response = client.get(
       f"/comments/1")
   print(response.json())
   assert response.status_code == 401


# Test Update POI - No Auth
def test_update_comment_no_auth(client):
    comment_data = {"comment": "updated", "creator": 1, "commented_poi": 1, "published": True }
    response = client.put("/comments/1",json=comment_data)
    assert response.status_code == 401

# Test for get All comments route - Authenticated User
def test_authorized_get_all_comments(client_auth, test_comments):
    response = client_auth.get(
        "/comments")
    print(response.json())
    print(test_comments)
    assert response.status_code == 200
    # assert len(response.json()) == len(test_comments)

# Test for Creating POI
def test_create_comment_auth(client_auth, test_user, test_pois):
    comment_data = {"comment": "test", "commented_poi": test_pois[0]['id'], "published": True, "creator": test_user['id'] }
    response = client_auth.post("/comments", json=comment_data)
    created_comment = schemas.Comment(**response.json())
    assert response.status_code == 201
    assert created_comment.comment == comment_data.comment
    assert created_comment.creator == test_user['id']
    assert created_comment.published == True


# Test for Find By Id - Auth User
def test_get_comment_by_id(client_auth, test_comments):
    response = client_auth.get(
        f"/comments/1")
    found_comment = schemas.Comment(**response.json())
    test_comment = test_comments[0]
    assert found_comment.Comment.title == test_comment['title']
    assert response.status_code == 200

    
# Test Update POI - Auth
def test_update_comment(client_auth, test_comments, test_user):
    comment_data = {"comment": "test comment", "commented_poi": 1, "published": True, "creator": test_user['id'] }
    response = client_auth.put("/comments/1",json= comment_data)
    updated_comment = schemas.Comment(**response.json())
    assert response.status_code == 201
    assert updated_comment.title == comment_data['title']
    assert updated_comment.description == comment_data['description']
    assert updated_comment.category == comment_data['category']
    assert updated_comment.lat == comment_data['lat']
    assert updated_comment.lng == comment_data['lng']
    assert updated_comment.creator == comment_data['creator']


# Test Delete POI - No Atuh
def test_delete_comment(client, test_comments):
    response = client.delete("/comments/1")
    assert response.status_code == 401

# Test Authenticated User Delete POI 
def test_delete_comment(client_auth, test_comments):
    response = client_auth.delete("/comments/1")
    assert response.status_code == 204

