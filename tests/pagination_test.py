from http import HTTPStatus
import os
import json
import pytest
import requests
import jsonschema
import requests
from requests import Response
from load_schema_helper import load_schema


def test_users_pagination_ok(app_url):
    response = requests.get(f"{app_url}/api/users/?page=1&size=1")
    assert response.status_code == HTTPStatus.OK

def test_users_pagination_minimal_values(app_url):
    response = requests.get(f"{app_url}/api/users/?page=1&size=1")
    assert len(response.json()["items"]) == 1
    assert response.json()["total"] == 12
    assert response.json()["page"] == 1
    assert response.json()["size"] == 1
    assert response.json()["pages"] == 12


def test_users_pagination_page_zero(app_url):
    response = requests.get(f"{app_url}/api/users/?page=0&size=1")
    schema = load_schema("unprocessable_entity_zero.json")
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    jsonschema.validate(response.json(), schema)
def test_users_pagination_size_zero(app_url):
    response = requests.get(f"{app_url}/api/users/?page=1&size=0")
    schema = load_schema("unprocessable_entity_zero.json")
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    jsonschema.validate(response.json(), schema)

def test_users_pagination_size_101(app_url):
    response = requests.get(f"{app_url}/api/users/?page=1&size=101")
    schema = load_schema("unprocessable_entity_101.json")
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    jsonschema.validate(response.json(), schema)

def test_users_without_pagination(app_url):
    response = requests.get(f"{app_url}/api/users/")
    assert response.status_code == HTTPStatus.OK
    assert len(response.json()["items"]) == 12
    assert response.json()["total"] == 12
    assert response.json()["page"] == 1
    assert response.json()["size"] == 50
    assert response.json()["pages"] == 1

@pytest.mark.parametrize("page", ["fafaf"])
def test_user_page_string(app_url, page):
    response = requests.get(f"{app_url}/api/users/?page={page}")
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

@pytest.mark.parametrize("size", ["fafaf"])
def test_user_size_string(app_url, size):
    response = requests.get(f"{app_url}/api/users/?size={size}")
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

@pytest.mark.parametrize("page, size", [(12, 1), (1, 12), (6, 2), (2, 6)])
def test_users_successful_pagination(app_url, page, size):
    response = requests.get(f"{app_url}/api/users/?size={size}&page={page}")
    assert response.status_code == HTTPStatus.OK
    assert response.json()["total"] == page * size
    assert response.json()["page"] == page
    assert response.json()["size"] == size
    assert response.json()["pages"] == (page * size) / size
    assert len(response.json()) == 5