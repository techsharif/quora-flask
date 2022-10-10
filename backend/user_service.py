from passlib.hash import sha256_crypt

from ResponseStatusException import ResponseStatusException
from database import get_user_by_email, create_user


def encrypt_password(password):
    return sha256_crypt.encrypt(password)


def match_password(raw_password, encrypted_password):
    return sha256_crypt.verify(raw_password, encrypted_password)


def verify_login(email, password):
    user = get_user_by_email(email)

    if user:
        if not match_password(password, user['password']):
            print("password not matched")
            raise ResponseStatusException(401, "Invalid credentials")
    else:
        print("User not found with email", email)
        raise ResponseStatusException(401, "Invalid credentials")


def verify_and_create_user(username, email, password):
    user = get_user_by_email(email)
    if user:
        raise ResponseStatusException(400, "User with this email already exists")

    password = encrypt_password(password)

    return create_user(username, email, password)
