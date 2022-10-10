from datetime import datetime

from bson import ObjectId
from pymongo import MongoClient

from ResponseStatusException import ResponseStatusException


class DB:
    def __init__(self):
        # self.client = MongoClient('mongodb://127.0.0.1', 27017)
        self.client = MongoClient('mongodb://root:password@127.0.0.1', 27017)
        self.db = self.client.userdatabase
        self.userCollection = self.db["users"]
        self.postCollection = self.db["posts"]
        self.commentCollection = self.db["comments"]
        print("Database Initiated")


db = DB()


def get_user_by_email(email):
    try:
        return db.userCollection.find_one({"email": email})
    except Exception as e:
        print(e)
        return None


def get_user_by_id(id):
    try:
        return db.userCollection.find_one({"_id": ObjectId(id)})
    except Exception as e:
        print(e)
        return None


def create_user(username, email, password):
    try:
        db.userCollection.insert_one({
            "username": username,
            "email": email,
            "password": password,
            "posts": [],
            "created_at": str(datetime.now()),  # todo: timezone
            "updated_at": str(datetime.now()),
        })

        return get_user_by_email(email)

    except Exception as e:
        print(e)
        raise ResponseStatusException(400, "Unable to create user")


def create_post(email, title):  # lookup can be another solution
    user = get_user_by_email(email)
    if not user:
        raise ResponseStatusException(400, "Invalid user")
    posts = user["posts"]
    post = {
        "id": len(posts) + 1,
        "title": title,
        "comments": [],
        "created_at": str(datetime.now()),  # todo: timezone
        "updated_at": str(datetime.now()),
    }
    db.userCollection.update_one({"email": email}, {"$set": {"posts": posts + [post]}})


def create_comment(email, postId, title):
    user = get_user_by_email(email)
    if not user:
        raise ResponseStatusException(400, "Invalid user")

    posts = user["posts"]

    if len(posts) <= postId:
        raise ResponseStatusException(400, "Invalid post")

    post = user["posts"][postId - 1]
    comments = post["comments"]
    comment = {
        "id": len(comments) + 1,
        "title": title,
        "created_at": str(datetime.now()),  # todo: timezone
        "updated_at": str(datetime.now()),
    }
    post["comments"] += [comment]

    db.userCollection.update_one({"email": email}, {"$set": {"posts": posts}})
