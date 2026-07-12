import json

import requests

BACKEND_URL = "http://127.0.0.1:8000"

LOGIN_ENDPOINT = f"{BACKEND_URL}/auth/login"
REGISTER_ENDPOINT = f"{BACKEND_URL}/auth/register"

def register(email, password):
    data = {
        "email": email,
        "password": password
    }
    with requests.Session() as session:
        response = requests.post(REGISTER_ENDPOINT, json=json.dumps(data))
    print(response.json())

if __name__ == "__main__":
    register()
