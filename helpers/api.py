import random
import string
import requests
from helpers.urls import COURIER, COURIER_LOGIN

def generate_random_string(length=10):
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for _ in range(length))

def build_courier_payload(login=None, password=None, first_name=None):
    return {
        "login": login if login is not None else generate_random_string(),
        "password": password if password is not None else generate_random_string(),
        "firstName": first_name if first_name is not None else generate_random_string(),
    }

def login_courier(login, password):
    return requests.post(
        COURIER_LOGIN,
        json={"login": login, "password": password},
        timeout=20,
    )

def delete_courier(courier_id):
    if courier_id:
        requests.delete(f"{COURIER}/{courier_id}", timeout=20)

def _delete_by_credentials(login, password):
    try:
        login_response = login_courier(login, password)
        if login_response.status_code == 200:
            delete_courier(login_response.json().get("id"))
    except Exception:
        pass