from ResponseStatusException import ResponseStatusException
from database import get_user_by_email, create_user


def verify_login(email, password):
    user = get_user_by_email(email)

    if user:
        if user['password'] != password:
            print("password not matched")
            raise ResponseStatusException(401, "Invalid credentials")
    else:
        print("User not found with email", email)
        raise ResponseStatusException(401, "Invalid credentials")


def verify_and_create_user(username, email, password):
    user = get_user_by_email(email)
    if user:
        raise ResponseStatusException(400, "User with this email already exists")

    return create_user(username, email, password)
