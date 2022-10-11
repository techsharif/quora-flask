from urllib import request

from flask import Flask, render_template, make_response, request, redirect, url_for, session
from flask_restful import Api, Resource

from auth import login, logout, get_message
from request_service import login_request, signup_request, home_request, user_request, create_post_request, \
    create_comment_request, delete_post_request, delete_comment_request
# import bcrypt
from utils import process_redirect_to

app = Flask(__name__)
api = Api(app)

app.secret_key = 'super secret key'


class Home(Resource):
    def get(self):
        error, message = get_message()
        posts = home_request()
        redirect_to = ""
        return make_response(
            render_template("home.html", error=error, message=message, posts=posts, redirect_to=redirect_to,
                            create_post=True),
            200)


class User(Resource):
    def get(self, username):
        error, message = get_message()
        posts = user_request(username)
        redirect_to = username
        return make_response(
            render_template("home.html", error=error, message=message, posts=posts, redirect_to=redirect_to,
                            create_post=username == session["username"]),
            200)


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


class Post(Resource):

    def get(self, post_id):
        redirect_to = process_redirect_to(request.args.get("redirect_to"))
        try:
            delete_post_request(post_id)
        except Exception as e:
            session["error"] = str(e)
        return redirect(redirect_to)

    def post(self):
        title = request.form.get("title")
        redirect_to = process_redirect_to(request.form.get("redirect_to"))
        try:
            create_post_request(title)
        except Exception as e:
            session["error"] = str(e)
        return redirect(redirect_to)


class Comment(Resource):

    def get(self, post_id, comment_id):
        redirect_to = process_redirect_to(request.args.get("redirect_to"))
        try:
            delete_comment_request(post_id, comment_id)
        except Exception as e:
            session["error"] = str(e)
        return redirect(redirect_to)

    def post(self, post_id):
        title = request.form.get("title")
        redirect_to = process_redirect_to(request.form.get("redirect_to"))
        try:
            create_comment_request(post_id, title)
        except Exception as e:
            session["error"] = str(e)

        return redirect(redirect_to)


api.add_resource(Home, "/", "/home")
api.add_resource(Login, "/login")
api.add_resource(Signup, "/signup")
api.add_resource(Logout, "/logout")
api.add_resource(User, "/user/<username>")
api.add_resource(Post, "/post", "/post/delete/<post_id>")
api.add_resource(Comment, "/comment/<post_id>", "/comment/delete/<post_id>/<comment_id>")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5008, debug=True)
