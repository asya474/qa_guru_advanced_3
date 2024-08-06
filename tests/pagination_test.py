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
    schema = load_schema("unprocessable_entity.json")
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    jsonschema.validate(response.json(), schema)
def test_users_pagination_size_zero(app_url):
    response = requests.get(f"{app_url}/api/users/?page=1&size=0")
    schema = load_schema("unprocessable_entity.json")
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    jsonschema.validate(response.json(), schema)

