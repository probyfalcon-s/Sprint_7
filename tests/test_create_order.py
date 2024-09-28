import allure
import requests

from conftest import generate_random_string
from src.config import ORDER_URL


class TestCreateOrder:
    def create_order(self, generate_random_string, color: list = None):
        payload = {
            "firstName": generate_random_string(10),
            "lastName": generate_random_string(10),
            "address": generate_random_string(15),
            "metroStation": "3",
            "phone": "+7 916 000 00 00",
            "rentTime": 4,
            "deliveryDate": "2024-10-30",
            "comment": "Test",
            "color": color if color else [],
        }

        return requests.post(ORDER_URL, json=payload)

    def test_create_order_black_color(self, generate_random_string):
        with allure.step(f"Создание заказа с цветом черный"):
            response = self.create_order(generate_random_string, color=["BLACK"])

        assert (
            response.status_code == 201
        ), f"Ожидаю 201, а получил {response.status_code}"
        assert "track" in response.json(), "Ответ должен содержать 'track'"

    def test_create_order_grey_color(self, generate_random_string):
        with allure.step(f"Создание заказа с цветом серый"):
            response = self.create_order(generate_random_string, color=["GREY"])

        assert (
            response.status_code == 201
        ), f"Ожидаю 201, а получил  {response.status_code}"
        assert "track" in response.json(), "Ответ должен содержать  'track'"

    def test_create_order_both_colors(self, generate_random_string):
        with allure.step(f"Создание заказа с обоими цветами"):
            response = self.create_order(
                generate_random_string, color=["BLACK", "GREY"]
            )

        assert (
            response.status_code == 201
        ), f"Ожидаю 201, а получил  {response.status_code}"
        assert "track" in response.json(), "Ответ должен содержать  'track'"

    def test_create_order_without_color(self, generate_random_string):
        with allure.step(f"Создание заказа без цвета"):
            response = self.create_order(generate_random_string, color=[])

        assert (
            response.status_code == 201
        ), f"Ожидаю 201, а получил  {response.status_code}"
        assert "track" in response.json(), "Ответ должен содержать 'track'"
