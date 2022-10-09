from ResponseStatusException import ResponseStatusException
from database import get_user_by_email


def verify_login(email, password):
    user = get_user_by_email(email)

    if user:
        if user['password'] != password:
            print("password not matched")
            raise ResponseStatusException(401, "Invalid credentials")
    else:
        print("User not found with email", email)
        raise ResponseStatusException(401, "Invalid credentials")
