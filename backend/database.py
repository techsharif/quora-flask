from pymongo import MongoClient

from ResponseStatusException import ResponseStatusException


class DB:
    def __init__(self):
        # self.client = MongoClient('mongodb://127.0.0.1', 27017)
        self.client = MongoClient('mongodb://root:password@127.0.0.1', 27017)
        self.db = self.client.userdatabase
        self.userCollection = self.db["users"]
        self.postCollection = self.db["post"]
        self.commentCollection = self.db["comment"]
        print("Database Initiated")


db = DB()


def get_user_by_email(email):
    try:
        return db.userCollection.find({"email": email})[0]
    except Exception as e:
        print(e)
        return None


def create_user(username, email, password):
    try:
        item = db.userCollection.insert_one({
            "username": username,
            "email": email,
            "password": password
        })

        return {
            "id": str(item.inserted_id),
            username: username,
            email: email,
            password: password
        }
    except Exception as e:
        print(e)
        raise ResponseStatusException(400, "Unable to create user")