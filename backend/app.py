from urllib import request
from urllib import request

from flask import Flask, request
from flask_restful import Api, Resource

from decorators import response_filter
from login_service import verify_login
from validator import validate_email, validate_password

# import bcrypt

app = Flask(__name__)
api = Api(app)


class Login(Resource):

    @response_filter
    def post(self):
        postedData = request.get_json()
        email = validate_email(postedData["email"])
        password = validate_password(postedData["password"])
        verify_login(email, password)


# class Signup(Resource):
#     def post(self):
#         postedData = request.get_json()
#
#         username = postedData["username"]
#         email = postedData["email"]
#         password = postedData["password"]
#
#         if len(password) < 6:
#             return jsonify({
#                 "status": 400,
#                 "error": "Password is too short"
#             })
#
#         if len(username) < 3:
#             return jsonify({
#                 "status": 400,
#                 "error": "Username is too short"
#             })
#
#         if not username.isalnum() or " " in username:
#             return jsonify({
#                 "status": 400,
#                 "error": "Username should be alphanumeric, also no spaces"
#             })
#
#         if not validators.email(email):
#             return jsonify({
#                 "status": 400,
#                 'error': "Email is not valid"
#             })
#
#         users.insert_one({
#             "username": username,
#             "email": email,
#             "password": password
#         })
#
#         retJson = {
#             "status": 200,
#             "msg": "You successfully signed up for the API"
#         }
#
#         return jsonify(retJson)
#
#

# api.add_resource(Home, "/", "/home")
api.add_resource(Login, "/login")
# api.add_resource(Signup, "/signup")

if __name__ == "__main__":
    app.run(debug=True)
