from urllib import request

from flask import Flask, request
from flask_restful import Api, Resource

from authentication import auth
from database import create_post, create_comment, get_all_post, delete_post, delete_comment, get_all_post_by_username, \
    get_filtered_post
from decorators import response_filter
from user_service import verify_and_create_user
from user_service import verify_login
from validator import validate_email, validate_password, validate_username, validate_title, validate_id

# import bcrypt

app = Flask(__name__)
api = Api(app)


class Login(Resource):  # hash password getting on get api

    @response_filter
    def post(self):
        postedData = request.get_json()
        username = validate_username(postedData["username"])
        password = validate_password(postedData["password"])
        verify_login(username, password)


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
        print("home")
        searchItem = request.args.get("search", "").strip()
        if searchItem:
            return get_filtered_post(searchItem)
        else:
            return get_all_post()


class User(Resource):

    @response_filter
    @auth.login_required
    def get(self, username):
        return get_all_post_by_username(username)


class Post(Resource):

    @response_filter
    @auth.login_required
    def post(self):
        postedData = request.get_json()
        title = validate_title(postedData["title"])
        create_post(auth.username(), title)

    @response_filter
    @auth.login_required
    def delete(self, postId):
        delete_post(postId, auth.username())


class Comment(Resource):

    @response_filter
    @auth.login_required
    def post(self, postId):
        postedData = request.get_json()
        postId = validate_id(postId)
        title = validate_title(postedData["title"])
        create_comment(auth.username(), postId, title)

    @response_filter
    @auth.login_required
    def delete(self, postId, commentId):
        postId = validate_id(postId)
        commentId = validate_id(commentId)
        delete_comment(postId, commentId, auth.username())


api.add_resource(Home, "/")
api.add_resource(User, "/<username>")
api.add_resource(Post, "/post", "/post/<postId>")
api.add_resource(Comment, "/comment/<postId>", "/comment/<postId>/<commentId>")
api.add_resource(Login, "/login")
api.add_resource(SignUp, "/signup")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5007, debug=True)
