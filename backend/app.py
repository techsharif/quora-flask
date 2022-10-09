import re
from urllib import request
from flask import Flask, jsonify, render_template, make_response, request
from flask_restful import Api, Resource
from pymongo import MongoClient
import bcrypt
import validators
from os import access

app = Flask(__name__)
api = Api(app)

client = MongoClient('mongodb://127.0.0.1', 27017)
db = client.userdatabase
users = db["users"]


class Home(Resource):
    def get(self):
        return make_response(render_template("home.html"), 200)


class Login(Resource):
    def get(self):
        return make_response(render_template("login.html"), 200)

    def post(self):
        postedData = request.get_json()

        email = postedData["email"]
        password = postedData["password"]

        correct_pw = verifyPw(email, password)

        if not correct_pw:
            retJson = {
                "status": 302,
                "msg": "Mismatch"
            }
        else:
            retJson = {
                "status": 200,
                "msg": "Successfully logged in"
            }

        return jsonify(retJson)


class Signup(Resource):
    def get(self):
        return make_response(render_template("signup.html"), 200)

    def post(self):
        postedData = request.get_json()

        username = postedData["username"]
        email = postedData["email"]
        password = postedData["password"]

        if len(password) < 6:
            return jsonify({
                "status": 400,
                "error": "Password is too short"
            })

        if len(username) < 3:
            return jsonify({
                "status": 400,
                "error": "Username is too short"
            })

        if not username.isalnum() or " " in username:
            return jsonify({
                "status": 400,
                "error": "Username should be alphanumeric, also no spaces"
            })

        if not validators.email(email):
            return jsonify({
                "status": 400,
                'error': "Email is not valid"
            })

        # if users.find({"email": email}) is not None:
        #     return jsonify({
        #         "status": 400,
        #         'error': "Email is taken"
        #     })

        # if users.find({"username": username}) is not None:
        #     return jsonify({
        #         "status": 400,
        #         'error': "Username is taken"
        #     })

        users.insert_one({
            "username": username,
            "email": email,
            "password": password
        })

        retJson = {
            "status": 200,
            "msg": "You successfully signed up for the API"
        }

        return jsonify(retJson)


def verifyPw(email, password):
    emailcheck = users.find(
        {
            "email": email
        }
    )

    if emailcheck:
        if emailcheck[0]['password'] == password:
            return True
        else:
            return False
    else:
        return False


api.add_resource(Home, "/", "/home")
api.add_resource(Login, "/login")
api.add_resource(Signup, "/signup")


if __name__ == "__main__":
    app.run(debug=True)
