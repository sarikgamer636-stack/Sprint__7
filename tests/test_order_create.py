import allure
import pytest
import requests
from helpers.data import COLOR_VARIANTS, ORDER_BODY
from helpers.urls import ORDERS

@allure.epic("API Яндекс.Самокат")
@allure.feature("Создание заказа")
class TestOrderCreate:

    @allure.title("Создание заказа с разными вариантами цвета")
    @pytest.mark.parametrize("color", COLOR_VARIANTS)
    def test_create_order_with_different_colors(self, color):
        payload = ORDER_BODY.copy()
        payload["color"] = color
        with allure.step("Отправляем запрос на создание заказа"):
            response = requests.post(ORDERS, json=payload)
        with allure.step("Проверяем код ответа и наличие track"):
            assert response.status_code == 201
            assert "track" in response.json()
            assert isinstance(response.json()["track"], int)