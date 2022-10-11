from urllib import request

from flask import Flask, render_template, make_response, request, redirect, url_for, session
from flask_restful import Api, Resource

from auth import login, logout
from request_service import login_request, signup_request, home_request

# import bcrypt

app = Flask(__name__)
api = Api(app)

app.secret_key = 'super secret key'


class Home(Resource):
    def get(self):
        posts = home_request()
        print(posts)
        return make_response(render_template("home.html", posts=posts), 200)


class Login(Resource):
    def get(self):
        if session.get("username"):
            return redirect(url_for('home'))
        return make_response(render_template("login.html"), 200)

    def post(self):
        username = request.form.get("username")
        password = request.form.get("password")

        try:
            login_request(username, password)
            login(username, password)
            return redirect(url_for('home'))
        except Exception as e:
            print(e)
            return make_response(render_template("login.html", error=str(e)), 200)


class Signup(Resource):
    def get(self):
        if session.get("username"):
            return redirect(url_for('home'))
        return make_response(render_template("signup.html"), 200)

    def post(self):

        username = request.form.get("username")
        password = request.form.get("password")
        email = request.form.get("email")

        try:
            signup_request(username, email, password)
            login(username, password)
            return redirect(url_for('home'))
        except Exception as e:
            print(e)
            return make_response(render_template("signup.html", error=str(e)), 200)


class Logout(Resource):

    def get(self):
        logout()
        return redirect(url_for('login'))


api.add_resource(Home, "/", "/home")
api.add_resource(Login, "/login")
api.add_resource(Signup, "/signup")
api.add_resource(Logout, "/logout")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5008, debug=True)
