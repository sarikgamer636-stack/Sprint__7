import pytest
from helpers.api import *
from helpers.courier import *
from helpers.api import _delete_by_credentials

@pytest.fixture
def new_courier():
    creds = register_new_courier_and_return_login_password()
    login, password, first_name = creds
    yield {"login": login, "password": password, "firstName": first_name}
    _delete_by_credentials(login, password)

@pytest.fixture
def courier_payload():
    payload = build_courier_payload()
    yield payload
    _delete_by_credentials(payload["login"], payload["password"])