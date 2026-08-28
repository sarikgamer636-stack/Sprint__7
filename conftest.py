import pytest
import requests
from helpers.api import *
from helpers.courier import *
from helpers.urls import *

def _delete_by_credentials(login, password):
    try:
        login_response = login_courier(login, password)
        if login_response.status_code == 200:
            delete_courier(login_response.json().get("id"))
    except Exception:
        pass

@pytest.fixture
def new_courier():
    creds = register_new_courier_and_return_login_password()
    login, password, first_name = creds
    yield {"login": login, "password": password, "firstName": first_name}
    _delete_by_credentials(login, password)

@pytest.fixture
def created_courier():
    payload = build_courier_payload()
    response = requests.post(COURIER, data=payload)
    yield payload, response
    _delete_by_credentials(payload["login"], payload["password"])