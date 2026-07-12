from streamlit import session_state

import requests


BACKEND_URL = "http://127.0.0.1:8000"

LOGIN_ENDPOINT = f"{BACKEND_URL}/auth/login/"
REGISTER_ENDPOINT = f"{BACKEND_URL}/auth/register/"
PROFILE_ENDPOINT = f"{BACKEND_URL}/users/me/"
ITEMS_ENDPOINT = f"{BACKEND_URL}/items/"
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


def get_items() -> requests.Response:
    # Авторизованному пользователю backend вернёт его is_favorite.
    if session_state.get("access_token"):
        return request_with_authorization_header("GET", ITEMS_ENDPOINT)
    return requests.get(ITEMS_ENDPOINT)


def get_item(item_id: int) -> requests.Response:
    endpoint = f"{ITEMS_ENDPOINT}{item_id}/"

    if session_state.get("access_token"):
        return request_with_authorization_header("GET", endpoint)
    return requests.get(endpoint)


def get_favorites() -> requests.Response:
    return request_with_authorization_header("GET", FAVORITES_ENDPOINT)


def add_favorite(item_id: int) -> requests.Response:
    endpoint = f"{FAVORITES_ENDPOINT}{item_id}/"
    return request_with_authorization_header("POST", endpoint)


def remove_favorite(item_id: int) -> requests.Response:
    endpoint = f"{FAVORITES_ENDPOINT}{item_id}/"
    return request_with_authorization_header("DELETE", endpoint)


def create_item(payload: dict) -> requests.Response:
    return request_with_authorization_header(
        "POST",
        ITEMS_ENDPOINT,
        payload=payload,
    )


def update_item(item_id: int, payload: dict) -> requests.Response:
    endpoint = f"{ITEMS_ENDPOINT}{item_id}/"
    return request_with_authorization_header(
        "PATCH",
        endpoint,
        payload=payload,
    )


def delete_item(item_id: int) -> requests.Response:
    endpoint = f"{ITEMS_ENDPOINT}{item_id}/"
    return request_with_authorization_header("DELETE", endpoint)