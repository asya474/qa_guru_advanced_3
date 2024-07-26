from http import HTTPStatus

import pytest
import requests


@pytest.mark.parametrize("user_id", [1, 6, 12])
def test_users_pagination(app_url, user_id):
    response = requests.get(f"{app_url}/api/users/{user_id}?page=1&size=1")
    assert response.status_code == HTTPStatus.OK

@pytest.mark.parametrize("user_id", [1, 6, 12])
def test_users_pagination_len_items(app_url, user_id):
    response = requests.get(f"{app_url}/api/users/{user_id}?page=1&size=1")
    assert len(response.json()["items"]) == 1


@pytest.mark.parametrize("user_id", [1, 6, 12])
def test_users_pagination_total(app_url, user_id):
    response = requests.get(f"{app_url}/api/users/{user_id}?page=1&size=1")
    assert response.json()["total"] == 1

@pytest.mark.parametrize("user_id", [1, 6, 12])
def test_users_pagination_page(app_url, user_id):
    response = requests.get(f"{app_url}/api/users/{user_id}?page=1&size=1")
    assert response.json()["page"] == 1


@pytest.mark.parametrize("user_id", [1, 6, 12])
def test_users_pagination(app_url, user_id):
    response = requests.get(f"{app_url}/api/users/{user_id}?page=1&size=1")
    assert response.json()["size"] == 1

@pytest.mark.parametrize("user_id", [1, 6, 12])
def test_users_pagination(app_url, user_id):
    response = requests.get(f"{app_url}/api/users/{user_id}?page=1&size=1")
    assert response.json()["pages"] == 1