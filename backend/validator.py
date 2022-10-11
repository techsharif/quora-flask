import validators

from ResponseStatusException import ResponseStatusException


def validate_username(username: str):
    username = username.strip()
    if len(username) < 3:
        raise ResponseStatusException(400, "Username should be at least 3 characters")

    if not username.isalnum():
        raise ResponseStatusException(400, "Username should be alpha numeric")

    return username.lower()


def validate_password(password: str):
    password = password.strip()
    if len(password) < 6:
        raise ResponseStatusException(400, "Password should be at least 6 characters")

    if not password.isalnum():
        raise ResponseStatusException(400, "Username should be alpha numeric")

    return password


def validate_email(email: str):
    email = email.strip()
    if not validators.email(email):
        raise ResponseStatusException(400, "Email is  not valid")

    return email


def validate_title(title: str):
    title = title.strip()
    if len(title) < 10:
        raise ResponseStatusException(400, "Content should be at least 10 characters")
    return title


def validate_id(_id: str):
    _id = _id.strip()
    if len(_id) < 6:
        raise ResponseStatusException(400, "Invalid Id")
    return _id
