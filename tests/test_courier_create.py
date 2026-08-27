import allure
import pytest
import requests
from helpers.api import build_courier_payload, delete_courier, login_courier
from helpers.urls import COURIER

@allure.epic("API Яндекс.Самокат")
@allure.feature("Создание курьера")
class TestCourierCreate:

    @allure.title("Курьера можно создать")
    def test_create_courier_success(self):
        payload = build_courier_payload()
        response = requests.post(COURIER, data=payload)
        assert response.status_code == 201
        assert response.json() == {"ok": True}
        login_response = login_courier(payload["login"], payload["password"])
        delete_courier(login_response.json().get("id"))

    @allure.title("Нельзя создать двух одинаковых курьеров")
    def test_cannot_create_two_identical_couriers(self, new_courier):
        response = requests.post(COURIER, data=new_courier)
        assert response.status_code == 409
        assert "логин уже используется" in response.json()["message"]

    @allure.title("Для создания курьера нужны все обязательные поля")
    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_create_courier_requires_required_fields(self, missing_field):
        payload = build_courier_payload()
        payload.pop(missing_field)
        response = requests.post(COURIER, data=payload)
        assert response.status_code == 400
        assert "Недостаточно данных" in response.json()["message"]

    @allure.title("Успешный запрос - возвращает код 201 и ok: true")
    def test_create_courier_returns_correct_code_and_body(self):
        payload = build_courier_payload()
        response = requests.post(COURIER, data=payload)
        assert response.status_code == 201
        assert response.json().get("ok") is True
        login_response = login_courier(payload["login"], payload["password"])
        delete_courier(login_response.json().get("id"))

    @allure.title("Повторное создание с тем же логином - возвращает ошибку")
    def test_create_courier_with_existing_login_returns_error(self, new_courier):
        payload = {
            "login": new_courier["login"],
            "password": "anotherpass",
            "firstName": "anothername",
        }
        response = requests.post(COURIER, data=payload)
        assert response.status_code == 409
        assert "логин уже используется" in response.json()["message"]