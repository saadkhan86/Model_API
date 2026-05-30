from app.database.database import db
from bson.objectid import ObjectId
users_collection = db["users"]


def create_user(user: dict):
    user = users_collection.insert_one(user)
    print(user)
    return {"message": "user created successfully"}


def get_user_by_email(email: str):
    return users_collection.find_one({"email": email})


def get_user_by_id(user_id: str):
    return users_collection.find_one({"_id": ObjectId(user_id)})


def update_user_by_id(user_id: str, user: dict):
    return users_collection.update_one({"_id": ObjectId(user_id)}, {"$set": user})


def delete_user_by_id(user_id: str):
    return users_collection.delete_one({"_id": ObjectId(user_id)})
