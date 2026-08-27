import pytest
from helpers.api import delete_courier, login_courier
from helpers.courier import register_new_courier_and_return_login_password

@pytest.fixture
def new_courier():
    creds = register_new_courier_and_return_login_password()
    assert creds, "Не удалось зарегистрировать курьера"
    login, password, first_name = creds
    yield {"login": login, "password": password, "firstName": first_name}
    try:
        login_response = login_courier(login, password)
        if login_response.status_code == 200:
            delete_courier(login_response.json().get("id"))
    except Exception:
        pass