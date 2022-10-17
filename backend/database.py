import uuid
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
        self.postCollection.create_index(([('title', 'text')]))
        print("Database Initiated")


db = DB()


def get_user_by_email(email):
    try:
        return db.userCollection.find_one({"email": email})
    except Exception as e:
        print(e)
        return None


def get_user_by_username(username):
    try:
        return db.userCollection.find_one({"username": username})
    except Exception as e:
        print(e)
        return None


def get_user_by_id(id):
    try:
        return db.userCollection.find_one({"_id": ObjectId(id)})
    except Exception as e:
        print(e)
        return None


def get_post_by_id(id):
    try:
        return db.postCollection.find_one({"_id": ObjectId(id)})
    except Exception as e:
        print(e)
        return None


def get_all_post():
    return db.postCollection.find().sort("created_at", -1)


def get_filtered_post(searchItem):
    return db.postCollection.find({"$text": {"$search": searchItem}}, {"score": {"$meta": "textScore"}})


def get_all_post_by_username(username):
    return db.postCollection.find({"username": username}).sort("created_at", -1)


def create_user(username, email, password):
    try:
        db.userCollection.insert_one({
            "username": username,
            "email": email,
            "password": password,
            "created_at": str(datetime.now()),  # todo: timezone
            "updated_at": str(datetime.now()),
        })

        return get_user_by_email(email)

    except Exception as e:
        print(e)
        raise ResponseStatusException(400, "Unable to create user")


def create_post(username, title):  # lookup can be another solution
    db.postCollection.insert_one(
        {
            "title": title,
            "username": username,
            "comments": {
                "size": 0,
                "items": {}
            },
            "created_at": str(datetime.now()),  # todo: timezone
            "updated_at": str(datetime.now()),
        }
    )


def delete_post(postId, username):  # lookup can be another solution
    post = get_post_by_id(postId)
    if not post:
        raise ResponseStatusException(400, "Post not found")
    if post["username"] != username:
        raise ResponseStatusException(400, "Invalid permission")

    db.postCollection.delete_one({"_id": post["_id"]})


def get_post_by_id(postId):  # lookup can be another solution
    post = get_post_by_id(postId)
    if not post:
        raise ResponseStatusException(400, "Post not found")
    return post


def delete_comment(postId, commentId, username):  # lookup can be another solution
    post = get_post_by_id(postId)
    if not post:
        raise ResponseStatusException(400, "Post not found")

    comment = post["comments"]["items"].get(commentId)

    if not comment:
        raise ResponseStatusException(400, "Comment not found")

    if post["username"] != username and comment["username"] != username:
        raise ResponseStatusException(400, "Invalid permission")

    comments = post["comments"]
    comments["size"] -= 1
    del comments["items"][commentId]

    db.postCollection.update_one({"_id": ObjectId(postId)}, {"$set": {"comments": comments}})


def create_comment(username, postId, title):
    post = get_post_by_id(postId)
    if not post:
        raise ResponseStatusException(400, "Post not found")

    comments = post["comments"]
    comment_id = str(uuid.uuid4())
    comments["size"] += 1
    comments["items"][comment_id] = {
        "id": comment_id,
        "username": username,
        "title": title,
        "created_at": str(datetime.now()),  # todo: timezone
        "updated_at": str(datetime.now()),
    }

    db.postCollection.update_one({"_id": ObjectId(postId)}, {"$set": {"comments": comments}})
