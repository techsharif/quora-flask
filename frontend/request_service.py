import requests

API_URL = "http://127.0.0.1:5007"
LOGIN_URL = API_URL + "/login"
SIGNUP_URL = API_URL + "/signup"
POST_URL = API_URL + "/post"
COMMENT_URL = API_URL + "/comment"
HOME_URL = API_URL


def login_request(username, password):
    response = requests.post(LOGIN_URL, json={'username': username, 'password': password})
    if response.status_code != 200:
        raise Exception(response.json().get("message"))

def signup_request(username, email, password):
    response = requests.post(SIGNUP_URL, json={'username': username, 'password': password, 'email': email})
    if response.status_code != 200:
        raise Exception(response.json().get("message"))

