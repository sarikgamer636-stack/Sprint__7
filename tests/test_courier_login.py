import allure
import pytest
import requests
from helpers.urls import COURIER_LOGIN

@allure.epic("API Яндекс.Самокат")
@allure.feature("Логин курьера")
class TestCourierLogin:

    @allure.title("Курьер может авторизоваться")
    def test_courier_can_login(self, new_courier):
        with allure.step("Отправляем запрос на авторизацию курьера"):
            response = requests.post(
            COURIER_LOGIN,
            json={"login": new_courier["login"], "password": new_courier["password"]},
            timeout=20,
        )
        with allure.step("Проверяем код ответа и id"):
            assert response.status_code == 200
            assert "id" in response.json()
            assert isinstance(response.json()["id"], int)

    @allure.title("Авторизация без логина возвращает ошибку")
    def test_login_without_login(self, new_courier):
        with allure.step("Отправляем запрос без логина"):
            response = requests.post(
            COURIER_LOGIN,
            json={"password": new_courier["password"]},
            timeout=20,
        )
        with allure.step("Проверяем код ответа и текст ошибки"):
            assert response.status_code == 400
            assert "Недостаточно данных" in response.json()["message"]

    @allure.title("Авторизация с пустым паролем возвращает ошибку")
    def test_login_with_empty_password(self, new_courier):
        with allure.step("Отправляем запрос с пустым паролем"):
            response = requests.post(
                COURIER_LOGIN,
                json={"login": new_courier["login"], "password": ""},
                timeout=20,
        )
        with allure.step("Проверяем код ответа и текст ошибки"):
            assert response.status_code in (400, 404)
            assert "message" in response.json()

    @allure.title("Ошибка при неверном логине или пароле")
    @pytest.mark.parametrize(
        "login_override,password_override",
        [
            (None, "wrongpassword"),
            ("wronglogin", None),
        ],
    )
    def test_login_wrong_credentials(self, new_courier, login_override, password_override):
        payload = {
            "login": login_override or new_courier["login"],
            "password": password_override or new_courier["password"],
        }
        with allure.step("Отправляем запрос с неверным логином или паролем"):
            response = requests.post(COURIER_LOGIN, json=payload, timeout=20)
        with allure.step("Проверяем код ответа и текст ошибки"):
            assert response.status_code == 404
            assert "Учетная запись не найдена" in response.json()["message"]

    @allure.title("Авторизация под несуществующим пользователем возвращает ошибку")
    def test_login_nonexistent_user(self):
        with allure.step("Отправляем запрос под несуществующим пользователем"):
            response = requests.post(
            COURIER_LOGIN,
            json={"login": "nouser_qweasdzxc", "password": "nouserpass"},
            timeout=20,
        )
        with allure.step("Проверяем код ответа и текст ошибки"):
            assert response.status_code == 404
            assert "Учетная запись не найдена" in response.json()["message"]

    @allure.title("Успешный запрос возвращает id")
    def test_login_success_returns_id(self, new_courier):
        with allure.step("Отправляем запрос на авторизацию курьера"):
            response = requests.post(
            COURIER_LOGIN,
            json={"login": new_courier["login"], "password": new_courier["password"]},
            timeout=20,
        )
        with allure.step("Проверяем, что в ответе есть id"):
            assert response.status_code == 200
            assert response.json().get("id")