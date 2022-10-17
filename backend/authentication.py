from flask_httpauth import HTTPBasicAuth

from user_service import verify_login

auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(email, password):
    verify_login(email, password)
    return True
