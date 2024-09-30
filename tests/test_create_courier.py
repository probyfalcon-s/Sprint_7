import pytest
import allure
import requests
from src.config import COURIER_URL
from src.helpers import generate_random_string
from src.api_requests import create_courier


class TestCreateCourier:
    @allure.title("Создание курьера")
    def test_create_courier_done(self, generate_random_string):
        login = generate_random_string(10)
        password = generate_random_string(10)
        first_name = generate_random_string(10)

        response = create_courier(login, password, first_name)

        assert (
            response.status_code == 201
        ), f"Ожидаю 201, а получил {response.status_code}"
        assert response.json().get("ok") is True, "Тело состоит из {'ok': true}"

    @allure.title("Невозможность создать двух одинаковых курьеров")
    def test_create_duplicate_courier(self, generate_random_string):
        login = generate_random_string(10)
        password = generate_random_string(10)
        first_name = generate_random_string(10)

        create_courier(login, password, first_name)

        response = create_courier(login, password, first_name)

        assert (
            response.status_code == 409
        ), f"Ожидаю 409, а получил {response.status_code}"
        assert (
            "Этот логин уже используется" in response.text
        ), "Этот логин уже используется"

    @allure.title("Передача всех обязательных полей")
    @pytest.mark.xfailed
    @pytest.mark.parametrize("missing_field", ["login", "password", "firstName"])
    def test_create_courier_missing_fields(self, generate_random_string, missing_field):
        data = {
            "login": generate_random_string(10),
            "password": generate_random_string(10),
            "firstName": generate_random_string(10),
        }

        del data[missing_field]

        response = requests.post(COURIER_URL, json=data)

        assert (
            response.status_code == 400
        ), f"Ожидаю 400 ошибку {missing_field}, получаю {response.status_code}"
        assert (
            "Недостаточно данных для создания учетной записи" in response.text
        ), "Недостаточно данных для создания учетной записи"

    @allure.title("Проверка кода ответа")
    def test_correct_code(self, generate_random_string):
        login = generate_random_string(10)
        password = generate_random_string(10)
        first_name = generate_random_string(10)

        response = create_courier(login, password, first_name)

        assert (
            response.status_code == 201
        ), f"ожидаю 201, получаю {response.status_code}"

    @allure.title("Успешный запрос возвращает {'ok' true}")
    def test_successful_response_contains(self, generate_random_string):
        login = generate_random_string(10)
        password = generate_random_string(10)
        first_name = generate_random_string(10)

        response = create_courier(login, password, first_name)

        assert response.json().get("ok") is True, "ожидаю {'ok': True} в ответе"

    @allure.title("ошибка, если нет одного из полей")
    def test_create_courier_missing_field_error(self, generate_random_string):
        login = generate_random_string(10)
        password = generate_random_string(10)

        payload = {"login": login, "password": password}

        response = requests.post(COURIER_URL, json=payload)

        assert response.status_code == 400, "Ожидаю 400"
        assert "Недостаточно данных для создания учетной записи" in response.text

    @allure.title("ошибка, если создать пользователя с уже существующим логином")
    @pytest.mark.xfailed
    def test_create_courier_returns_error(self, generate_random_string):
        login = generate_random_string(10)
        password = generate_random_string(10)
        first_name = generate_random_string(10)

        create_courier(login, password, first_name)

        response = create_courier(
            login, generate_random_string(10), generate_random_string(10)
        )

        assert (
            response.status_code == 409
        ), f"Ожидаю 409, получил {response.status_code}"
        assert (
            "Этот логин уже используется" in response.text
        ), "Этот логин уже используется"
