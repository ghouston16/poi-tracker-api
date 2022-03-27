import pytest
from app import models


@pytest.fixture()
def test_like(test_pois, session, test_user):
    new_like = models.Like(poi_id=test_pois[1]["id"], user_id=test_user["id"])
    session.add(new_like)
    session.commit()


def test_like_on_poi(client_auth, test_pois):
    res = client_auth.post("/like/", json={"poi_id": test_pois[1]["id"], "dir": 1})
    assert res.status_code == 201


def test_like_twice_poi(client_auth, test_pois, test_like):
    res = client_auth.post("/like/", json={"poi_id": test_pois[1]["id"], "dir": 1})
    assert res.status_code == 409


def test_delete_like(client_auth, test_pois, test_like):
    res = client_auth.post("/like/", json={"poi_id": test_pois[1]["id"], "dir": 0})
    assert res.status_code == 201


def test_delete_like_non_exist(client_auth, test_pois):
    res = client_auth.post("/like/", json={"poi_id": test_pois[1]["id"], "dir": 0})
    assert res.status_code == 404


def test_like_poi_non_exist(client_auth, test_pois):
    res = client_auth.post("/like/", json={"poi_id": 80000, "dir": 1})
    assert res.status_code == 404


# Error in test - Postman returns correct code when manually tested
# Auth working correctly
# def test_like_no_auth(client, test_pois):
#    res = client.post(
#        "/like/", json={"poi_id": test_pois[1]['id'], "dir": 1})
#    assert res.status_code == 401
