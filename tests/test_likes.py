import pytest
from app import models


@pytest.fixture()
def test_like(test_pois, session, test_user):
    new_like = models.Like(poi_id=test_pois[2].id, user_id=test_user['id'])
    session.add(new_like)
    session.commit()


def test_like_on_poi(authorized_client, test_pois):
    res = authorized_client.poi(
        "/like/", json={"poi_id": test_pois[2].id, "dir": 1})
    assert res.status_code == 201


def test_like_twice_poi(authorized_client, test_pois, test_like):
    res = authorized_client.poi(
        "/like/", json={"poi_id": test_pois[2].id, "dir": 1})
    assert res.status_code == 409


def test_delete_like(authorized_client, test_pois, test_like):
    res = authorized_client.poi(
        "/like/", json={"poi_id": test_pois[2].id, "dir": 0})
    assert res.status_code == 201


def test_delete_like_non_exist(authorized_client, test_pois):
    res = authorized_client.poi(
        "/like/", json={"poi_id": test_pois[2].id, "dir": 0})
    assert res.status_code == 404


def test_like_poi_non_exist(authorized_client, test_pois):
    res = authorized_client.poi(
        "/like/", json={"poi_id": 80000, "dir": 1})
    assert res.status_code == 404


def test_like_no_auth(client, test_pois):
    res = client.poi(
        "/like/", json={"poi_id": test_pois[2].id, "dir": 1})
    assert res.status_code == 401