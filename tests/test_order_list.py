import requests
import allure
from src.config import ORDER_URL


class TestOrderList:
    @staticmethod
    def get_order_list():
        return requests.get(ORDER_URL)

    def test_order_list_contains_orders(self):
        with allure.step(f"Тест: проверка, что список заказов содержит заказы"):
            response = self.get_order_list()

        assert (
            response.status_code == 200
        ), f"Ожидаю 200, получил {response.status_code}"

        response_json = response.json()
        assert "orders" in response_json, "Ответ должен содержать 'orders'"
        assert isinstance(response_json["orders"], list), "'orders' должно быть"
