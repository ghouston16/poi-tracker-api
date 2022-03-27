from ast import List
from random import randint
from fastapi.testclient import TestClient
from app.main import app
from app import schemas
import pytest


# Test for unauthenticated attempt to comment on a poi
def test_create_comment_no_auth(client):
    comment_data = {
        "comment": "comment 3",
        "creator": 1,
        "poi_id": 1,
        "published": True,
    }
    response = client.post(f"pois/{comment_data['poi_id']}/comments", json=comment_data)
    print(response.json())
    assert response.status_code == 401  # Unauthorized


# Test for get All comments route unauthenticated
def test_no_auth_get_all_poi_comments(client):
    response = client.get(f"pois/1/comments")
    print(response.json())
    assert response.status_code == 401  # Unauthorized


# Test for comment Find By Id - No Auth User
def test_get_comment_by_id_no_auth(client):
    response = client.get(f"/pois/comments/1")
    print(response.json())
    assert response.status_code == 401  # Unauthorized


# Test Update comment - No Auth
def test_update_comment_no_auth(client):
    comment_data = {"comment": "updated", "creator": 1, "poi_id": 1, "published": True}
    response = client.put(
        f"pois/{comment_data['poi_id']}/comments/1", json=comment_data
    )
    assert response.status_code == 401  # Unauthorized


# Test for Creating POI Comment
def test_create_comment_auth(client_auth, test_user, test_pois):
    comment_data = {
        "comment": "test",
        "poi_id": test_pois[0]["id"],
        "published": True,
        "creator": test_user["id"],
    }
    response = client_auth.post(
        f"pois/{comment_data['poi_id']}/comments", json=comment_data
    )
    created_comment = schemas.Comment(**response.json())
    assert response.status_code == 201  # Content Created
    assert created_comment.comment == comment_data["comment"]
    assert created_comment.creator == test_user["id"]
    assert created_comment.published == True


# Test for Find By Id - Auth User
def test_get_comments_by_poi_id(client_auth, test_comments):
    response = client_auth.get(f"/pois/{test_comments[0]['poi_id']}/comments")
    found_comments = response.json()
    comment = schemas.CommentOut(**found_comments[0])
    test_comment = test_comments[0]
    assert comment.poi_id == test_comment["poi_id"]
    assert response.status_code == 200


# Test Update POI - Auth
def test_update_comment_auth(client_auth, test_comments, test_user):
    comment_data = {
        "id": 1,
        "comment": "test comment",
        "poi_id": 1,
        "creator": test_user["id"],
    }
    response = client_auth.put(
        f"/pois/{test_comments[0]['poi_id']}/comments/{comment_data['id']}",
        json=comment_data,
    )
    updated_comment = schemas.CommentOut(**response.json())
    assert response.status_code == 201  # Comment Update Created
    assert updated_comment.comment == comment_data["comment"]
    assert updated_comment.poi_id == comment_data["poi_id"]


# Test Delete POI - No Atuh
def test_delete_comment(client):
    response = client.delete(f"/pois/1/comments/1")
    assert response.status_code == 401  # Unauthorized


# Test Authenticated User Delete POI
def test_delete_comment_auth(client_auth, test_comments, test_user):
    response = client_auth.delete(
        f"/pois/{test_comments[0]['poi_id']}/comments/{test_comments[0]['id']}"
    )
    assert response.status_code == 204  # No Content Found
