from flask import session


def login(username, password):
    session["username"] = username
    session["password"] = password


def logout():
    session["username"] = None
    session["password"] = None


def get_auth():
    return (session["username"], session["password"])


def get_message():
    error = session.get("error")
    message = session.get("message")
    session["error"] = None
    session["message"] = None

    return error, message
