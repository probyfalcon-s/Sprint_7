import allure
from src.api_requests import create_order
from src.helpers import generate_random_string


class TestCreateOrder:
    @allure.step("Создание заказа с цветом черный")
    def test_create_order_black_color(self, generate_random_string):
        random_string = generate_random_string(10)
        response = create_order(random_string=random_string, color=["BLACK"])

        assert (
            response.status_code == 201
        ), f"Ожидаю 201, а получил {response.status_code}"
        assert "track" in response.json(), "Ответ должен содержать 'track'"

    @allure.step("Создание заказа с цветом серый")
    def test_create_order_grey_color(self, generate_random_string):
        random_string = generate_random_string(10)
        response = create_order(random_string=random_string, color=["GREY"])

        assert (
            response.status_code == 201
        ), f"Ожидаю 201, а получил  {response.status_code}"
        assert "track" in response.json(), "Ответ должен содержать  'track'"

    @allure.step("Создание заказа с обоими цветами")
    def test_create_order_both_colors(self, generate_random_string):
        random_string = generate_random_string(10)
        response = create_order(random_string=random_string, color=["BLACK", "GREY"])

        assert (
            response.status_code == 201
        ), f"Ожидаю 201, а получил  {response.status_code}"
        assert "track" in response.json(), "Ответ должен содержать  'track'"

    @allure.step("Создание заказа без цвета")
    def test_create_order_without_color(self, generate_random_string):
        random_string = generate_random_string(10)
        response = create_order(random_string=random_string, color=[])

        assert (
            response.status_code == 201
        ), f"Ожидаю 201, а получил  {response.status_code}"

        assert "track" in response.json(), "Ответ должен содержать 'track'"
