from http import HTTPStatus

import requests


def test_status_ok(app_url):
    response = requests.get(f"{app_url}/status")
    assert response.status_code == HTTPStatus.OK


def test_status_ok(app_url):
    response = requests.get(f"{app_url}/status").json()
    assert response["users"]
