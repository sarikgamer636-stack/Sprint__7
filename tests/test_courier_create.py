import allure
import pytest
from helpers.api import *
from helpers.urls import COURIER

@allure.epic("API Яндекс.Самокат")
@allure.feature("Создание курьера")
class TestCourierCreate:

    @allure.title("Курьера можно создать")
    def test_create_courier_success(self, created_courier):
        payload, response = created_courier
        with allure.step("Проверяем код ответа и тело"):
            assert response.status_code == 201
            assert response.json() == {"ok": True}

    @allure.title("Нельзя создать двух одинаковых курьеров")
    def test_cannot_create_two_identical_couriers(self, new_courier):
        with allure.step("Отправляем запрос на создание курьера"):
            response = requests.post(COURIER, data=new_courier)
        with allure.step("Проверяем код ответа и текст ошибки"):
            assert response.status_code == 409
            assert "логин уже используется" in response.json()["message"]

    @allure.title("Для создания курьера нужны все обязательные поля")
    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_create_courier_requires_required_fields(self, missing_field):
        payload = build_courier_payload()
        payload.pop(missing_field)
        with allure.step("Отправляем запрос без обязательного поля"):
            response = requests.post(COURIER, data=payload)
        with allure.step("Проверяем код ответа и текст ошибки"):
            assert response.status_code == 400
            assert "Недостаточно данных" in response.json()["message"]
