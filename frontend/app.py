from urllib import request

from flask import Flask, render_template, request, redirect, url_for, session
from flask.views import MethodView

from auth import login, logout, get_message
from request_service import login_request, signup_request, home_request, user_request, create_post_request, \
    create_comment_request, delete_post_request, delete_comment_request, get_post_request
# import bcrypt
from utils import process_redirect_to

app = Flask(__name__)

app.secret_key = 'super secret key'


class Home(MethodView):

    def get(self):
        if not session.get("username"):
            return redirect(url_for('login'))
        error, message = get_message()
        search = request.args.get("search", "").strip()
        posts = home_request(search)
        redirect_to = "_home"
        return render_template("home.html", error=error, message=message, posts=posts, redirect_to=redirect_to,
                               create_post=True)


class User(MethodView):
    def get(self, username):
        error, message = get_message()
        posts = user_request(username)
        redirect_to = "_user_" + username
        return render_template("home.html", error=error, message=message, posts=posts, redirect_to=redirect_to,
                               create_post=username == session["username"])


class Login(MethodView):
    def get(self):
        if session.get("username"):
            return redirect(url_for('home'))
        return render_template("login.html")

    def post(self):
        username = request.form.get("username")
        password = request.form.get("password")

        try:
            login_request(username, password)
            login(username, password)
            return redirect(url_for('home'))
        except Exception as e:
            print(e)
            return render_template("login.html", error=str(e))


class Signup(MethodView):
    def get(self):
        if session.get("username"):
            return redirect(url_for('home'))
        return render_template("signup.html")

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
            return render_template("signup.html", error=str(e))


class Logout(MethodView):

    def get(self):
        logout()
        return redirect(url_for('login'))


class Post(MethodView):

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


class PostView(MethodView):
    def get(self, post_id):
        if not session.get("username"):
            return redirect(url_for('login'))

        error, message = get_message()
        post = get_post_request(post_id)
        redirect_to = "_details_" + post_id
        return render_template("post.html", error=error, message=message, post=post, redirect_to=redirect_to,
                               create_post=True)


class Comment(MethodView):

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


app.add_url_rule("/", view_func=Home.as_view("root"))
app.add_url_rule("/home", view_func=Home.as_view("home"))
app.add_url_rule("/login", view_func=Login.as_view("login"))
app.add_url_rule("/signup", view_func=Signup.as_view("signup"))
app.add_url_rule("/logout", view_func=Logout.as_view("logout"))
app.add_url_rule("/user/<username>", view_func=User.as_view("user"))
app.add_url_rule("/post", view_func=Post.as_view("post"))
app.add_url_rule("/details", view_func=PostView.as_view("details"))
app.add_url_rule("/post/delete/<post_id>", view_func=Post.as_view("delete-post"))
app.add_url_rule("/comment/<post_id>", view_func=Comment.as_view("comment"))
app.add_url_rule("/comment/delete/<post_id>/<comment_id>", view_func=Comment.as_view("delete-comment"))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5008, debug=True)
