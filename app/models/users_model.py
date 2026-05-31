from app.schema.user_schema import *
from app.database.database import users_collection
from app.error_handler.custom_exception import *
from bson.objectid import ObjectId
from pymongo import ReturnDocument


def create_user(data: UserSignUpSchema):
    user = data.model_dump()
    inserted_user = users_collection.insert_one(user)
    user["id"] = str(inserted_user.inserted_id)
    return UserResponseSchema(**user)


def get_user_by_email(email: str):
    return users_collection.find_one({"email": email})


def get_user_by_id(user_id: str):
    user = users_collection.find_one({"_id": ObjectId(user_id)})
    return UserResponseSchema(**user)


def update_user_by_id(user_id: str, data: UserUpdateSchema):
    dict_user = data.model_dump(exclude_unset=True)
    user = users_collection.find_one_and_update({"_id": ObjectId(user_id)}, {
                                                "$set": dict_user}, return_document=ReturnDocument.AFTER)
    if not user:
        raise CustomException(f"User not found for ID : {user_id}", 404)
    return UserResponseSchema(**user)


def delete_user_by_id(user_id: str):
    user = users_collection.delete_one({"_id": ObjectId(user_id)})
    return user.deleted_count > 0
