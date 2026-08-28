import allure
import requests
from helpers.urls import ORDERS

@allure.epic("API Яндекс.Самокат")
@allure.feature("Список заказов")
class TestOrderList:

    @allure.title("В теле ответа возвращается список заказов")
    def test_order_list_returns_orders_array(self):
        with allure.step("Отправляем запрос на получение списка заказов"):
            response = requests.get(ORDERS, params={"limit": 10}, timeout=40)
        with allure.step("Проверяем, что в ответе есть список orders"):
            assert response.status_code == 200
            body = response.json()
            assert "orders" in body
            assert isinstance(body["orders"], list)