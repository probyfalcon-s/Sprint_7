# Тест: успешное создание курьера
def test_create_courier():
    login, password, first_name, status_code, response_json = register_new_courier()

    assert status_code == 201, f"status code 201, but got {status_code}"
    assert response_json.get("ok") == True, f"Unexpected response: {response_json}"
    print("Courier successfully created.")


# Тест: дублирующее создание курьера
def test_create_duplicate_courier():
    # создаем первого курьера
    login, password, first_name, status_code, _ = register_new_courier()
    assert status_code == 201, f"Failed to create initial courier: {status_code}"

    # пробуем создать курьера с теми же данными
    payload = {"login": login, "password": password, "firstName": first_name}
    response = requests.post(BASE_URL, json=payload)

    # проверяем, что повторное создание курьера с тем же логином не допускается
    assert (
        response.status_code == 409
    ), f"Expected status code 409, but got {response.status_code}"
    assert (
        response.json().get("message") == "Этот логин уже используется"
    ), f"Unexpected error message: {response.json()}"
    print("Duplicate courier creation correctly blocked.")


# Тест: создание курьера с отсутствующими обязательными полями
def test_create_courier_missing_fields():
    # создаем курьера без пароля
    payload = {"login": "testlogin", "firstName": "testname"}
    response = requests.post(BASE_URL, json=payload)

    # проверяем, что сервер вернет ошибку 400
    assert (
        response.status_code == 400
    ), f"Expected status code 400, but got {response.status_code}"
    assert (
        response.json().get("message")
        == "Недостаточно данных для создания учетной записи"
    ), f"Unexpected error message: {response.json()}"
    print("Missing fields correctly handled.")
