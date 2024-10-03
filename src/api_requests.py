import allure
import requests
from requests import Response
from src.config import COURIER_URL, ORDER_URL, LOGIN_URL


@allure.step("функция для создания нового курьера")
def create_courier(login: str, password: str, first_name: str) -> Response:
    payload = {"login": login, "password": password, "firstName": first_name}
    return requests.post(COURIER_URL, json=payload)


@allure.step("Функция для создания заказа")
def create_order(random_string: str, color: list = None):
    payload = {
        "firstName": random_string,
        "lastName": random_string,
        "address": random_string + " Address",
        "metroStation": "3",
        "phone": "+7 916 000 00 00",
        "rentTime": 4,
        "deliveryDate": "2024-10-30",
        "comment": "Test",
        "color": color if color else [],
    }

    response = requests.post(ORDER_URL, json=payload)
    return response


@allure.step("Функция для регистрации нового курьера")
def register_new_courier(login: str, password: str, first_name: str):
    payload = {"login": login, "password": password, "firstName": first_name}
    return requests.post(COURIER_URL, json=payload)


@allure.step("Функция логирования курьера")
def login_courier(login: str, password: str):
    payload = {"login": login, "password": password}
    return requests.post(LOGIN_URL, json=payload)
