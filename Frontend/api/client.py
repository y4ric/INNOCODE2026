from streamlit import session_state

import requests


BACKEND_URL = "http://127.0.0.1:8000"

LOGIN_ENDPOINT = f"{BACKEND_URL}/auth/login/"
REGISTER_ENDPOINT = f"{BACKEND_URL}/auth/register/"
PROFILE_ENDPOINT = f"{BACKEND_URL}/users/me/"
CARS_ENDPOINT = f"{BACKEND_URL}/cars/"
FAVORITES_ENDPOINT = f"{BACKEND_URL}/favorites/"


def register(email: str, password: str, full_name: str) -> requests.Response:
    data = {
        "email": email,
        "password": password,
        "full_name": full_name,
    }
    return requests.post(REGISTER_ENDPOINT, json=data)


def login(email: str, password: str) -> requests.Response:
    data = {
        "email": email,
        "password": password,
    }
    return requests.post(LOGIN_ENDPOINT, json=data)


def request_with_authorization_header(
    request_type: str,
    endpoint: str,
    params: dict | None = None,
    payload: dict | None = None,
) -> requests.Response:
    headers = {
        "Authorization": f"Bearer {session_state['access_token']}"
    }

    if request_type == "GET":
        response = requests.get(endpoint, headers=headers, params=params)
    elif request_type == "POST":
        response = requests.post(endpoint, headers=headers, params=params, json=payload)
    elif request_type == "PATCH":
        response = requests.patch(endpoint, headers=headers, params=params, json=payload)
    elif request_type == "DELETE":
        response = requests.delete(endpoint, headers=headers, params=params)
    else:
        raise ValueError("Неизвестный тип запроса")

    # Если JWT больше не действителен, удаляем авторизацию.
    if response.status_code == 401:
        session_state.pop("access_token", None)
        session_state.pop("profile", None)

    return response


def get_error_message(response: requests.Response) -> str:
    try:
        detail = response.json().get("detail")
        return str(detail or f"Ошибка backend: HTTP {response.status_code}")
    except ValueError:
        return f"Ошибка backend: HTTP {response.status_code}"


def get_profile() -> requests.Response:
    return request_with_authorization_header("GET", PROFILE_ENDPOINT)


def get_cars() -> requests.Response:
    # Авторизованному пользователю backend вернёт его is_favorite.
    if session_state.get("access_token"):
        return request_with_authorization_header("GET", CARS_ENDPOINT)
    return requests.get(CARS_ENDPOINT)


def get_car(car_id: int) -> requests.Response:
    endpoint = f"{CARS_ENDPOINT}/{car_id}"

    if session_state.get("access_token"):
        return request_with_authorization_header("GET", endpoint)
    return requests.get(endpoint)


def get_favorites() -> requests.Response:
    # Явно импортируем streamlit, если его нет вверху файла
    import streamlit as st

    # Пытаемся достать ID пользователя. Если там None, ставим заглушку 1
    user_id = st.session_state.get("user_id") or 1

    # Важно передать params именно третьим аргументом в вашу функцию:
    return request_with_authorization_header(
        "GET",
        FAVORITES_ENDPOINT,
        params={"user_id": user_id}
    )


def add_favorite(car_id: int) -> requests.Response:
    endpoint = f"{FAVORITES_ENDPOINT}"

    user_id = session_state.get("user_id", 1)

    return request_with_authorization_header(
        "POST",
        endpoint,
        payload={
            "car_id": car_id,
            "user_id": user_id
        }
    )


def remove_favorite(car_id: int) -> requests.Response:
    import streamlit as st
    user_id = st.session_state.get("user_id") or 1

    # Склеиваем адрес со знаком вопроса и параметрами: /favorites/?car_id=...&user_id=...
    endpoint = f"{FAVORITES_ENDPOINT}/?car_id={car_id}&user_id={user_id}"

    return request_with_authorization_header("DELETE", endpoint)


def create_car(payload: dict) -> requests.Response:
    return request_with_authorization_header(
        "POST",
        CARS_ENDPOINT,
        payload=payload,
    )


def update_car(car_id: int, payload: dict) -> requests.Response:
    endpoint = f"{CARS_ENDPOINT}{car_id}/"
    return request_with_authorization_header(
        "PATCH",
        endpoint,
        payload=payload,
    )


def delete_car(car_id: int) -> requests.Response:
    endpoint = f"{CARS_ENDPOINT}{car_id}/"
    return request_with_authorization_header("DELETE", endpoint)