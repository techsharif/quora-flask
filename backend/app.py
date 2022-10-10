from urllib import request

from flask import Flask, request
from flask_restful import Api, Resource

from authentication import auth
from database import get_user_by_email, create_post, create_comment
from decorators import response_filter
from user_service import verify_and_create_user
from user_service import verify_login
from validator import validate_email, validate_password, validate_username, validate_title

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


class SignUp(Resource):
    @response_filter
    def post(self):
        postedData = request.get_json()
        username = validate_username(postedData["username"])
        email = validate_email(postedData["email"])
        password = validate_password(postedData["password"])

        return verify_and_create_user(username, email, password)


class Home(Resource):

    @response_filter
    @auth.login_required
    def get(self):
        return get_user_by_email(auth.username())


class Post(Resource):

    @response_filter
    @auth.login_required
    def post(self):
        postedData = request.get_json()
        title = validate_title(postedData["title"])
        create_post(auth.username(), title)
        return get_user_by_email(auth.username())


class Comment(Resource):

    @response_filter
    @auth.login_required
    def post(self):
        postedData = request.get_json()
        postId = int(postedData["postId"])
        title = validate_title(postedData["title"])
        create_comment(auth.username(), postId, title)
        return get_user_by_email(auth.username())


api.add_resource(Home, "/", "/home")
api.add_resource(Post, "/post")
api.add_resource(Comment, "/comment")
api.add_resource(Login, "/login")
api.add_resource(SignUp, "/signup")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5007, debug=True)
