import allure
import pytest
import requests
from src.config import LOGIN_URL
from src.api_requests import register_new_courier, login_courier
from src.helpers import generate_random_string


class TestLoginCourier:
    def test_courier_login(self, generate_random_string):
        with allure.step(f"Успешная регистрация курьера"):
            login = generate_random_string(10)
            password = generate_random_string(10)
            first_name = generate_random_string(10)

            register_response = register_new_courier(login, password, first_name)
            assert register_response.status_code == 201

        with allure.step("Логин курьера"):
            login_response = login_courier(login, password)

            assert login_response.status_code == 200, "Ожидаю 200 код"
            assert "id" in login_response.json(), "Ответ должен содержать 'id'"

    @pytest.mark.xfailed
    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_login_missing_fields(self, generate_random_string, missing_field):
        with allure.step(f"Ошибка при отсутствии обязательных полей"):
            data = {
                "login": generate_random_string(10),
                "password": generate_random_string(10),
            }

            del data[missing_field]

            response = requests.post(LOGIN_URL, json=data)

            assert (
                response.status_code == 400
            ), f"Ожидаю 400 код {missing_field}, получаю {response.status_code}"
            assert (
                "Недостаточно данных для входа" in response.text
            ), "Недостаточно данных для входа"

    @pytest.mark.parametrize(
        "login, password",
        [("wronglogin", "correctpassword"), ("correctlogin", "wrongpassword")],
    )
    def test_incorrect_login_password(self, login, password):
        with allure.step(f"случайный логин и пароль"):
            response = login_courier(login, password)

            assert (
                response.status_code == 404
            ), f"Ожидаю 404, получил {response.status_code}"
            assert (
                "Учетная запись не найдена" in response.text
            ), "Учетная запись не найдена"

    def test_login_nonexistent_user(self, generate_random_string):
        with allure.step(f"Логин несуществующим пользователем"):
            login = generate_random_string(10)
            password = generate_random_string(10)

            response = login_courier(login, password)

            assert response.status_code == 404, "Ожидаю 404 код"
            assert (
                "Учетная запись не найдена" in response.text
            ), "Учетная запись не найдена"

    def test_successful_login_returns_id(self, generate_random_string):
        with allure.step(f"Успешный логин возращает ID"):
            login = generate_random_string(10)
            password = generate_random_string(10)
            first_name = generate_random_string(10)

            register_response = register_new_courier(login, password, first_name)
            assert register_response.status_code == 201

            login_response = login_courier(login, password)

            assert login_response.status_code == 200, "Ожидаю 200 код"
            assert "id" in login_response.json(), "Ответ должен содержать 'id'"
