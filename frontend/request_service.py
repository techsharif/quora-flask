import requests

from auth import get_auth

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


def home_request():
    response = requests.get(HOME_URL, auth=get_auth())
    if response.status_code != 200:
        raise Exception(response.json().get("message"))
    return process_post_response(response.json())


def user_request(username):
    response = requests.get(HOME_URL + "/" + username, auth=get_auth())
    if response.status_code != 200:
        raise Exception(response.json().get("message"))
    return process_post_response(response.json())


def process_post_response(response):
    for post in response:
        post["id"] = post["_id"]["$oid"]
        post["comments"]["_items"] = process_comments(post["comments"]["items"])
    return response


def process_comments(items: dict):
    comments = list(items.values())
    comments.sort(key=lambda comment: comment["created_at"])
    return comments
