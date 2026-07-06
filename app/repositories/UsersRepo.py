from app.schema.user_schema import Signup, Return, Update
from app.config.database import users_collection
from app.error_handler.custom_exception import CustomException
from pymongo import ReturnDocument
from app.utils.to_object_id import to_object_id
from app.utils.validate_phone_numbers import get_normalized_number

class UsersRepo:
    def __init__(self):
        self.users_collection = users_collection

    def signup(self, data: Signup) -> Return:
        user_data = data.model_dump()
        user_data["phone_number"] = get_normalized_number(user_data["phone_number"])
        inserted_user = self.users_collection.insert_one(user_data)
        if not inserted_user.inserted_id:
            raise CustomException("User not created", 500)
        user_data["_id"] = str(inserted_user.inserted_id)
        return Return.model_validate(user_data)

    def get(self, user_id: str) -> Return:
        user_data = self.users_collection.find_one(
            {"_id": to_object_id(user_id)})
        if not user_data:
            raise CustomException("User not found", 404)
        return Return.model_validate(user_data)

    def update(self, user_id: str, data: Update) -> Return:
        new_data = data.model_dump(exclude_unset=True)
        user_data = self.users_collection.find_one_and_update({"_id": to_object_id(user_id)}, {
            "$set": new_data}, return_document=ReturnDocument.AFTER)
        if not user_data:
            raise CustomException(f"User not found for ID : {user_id}", 404)
        return Return.model_validate(user_data)

    def delete(self, user_id: str) -> bool:
        user_data = self.users_collection.delete_one(
            {"_id": to_object_id(user_id)})
        if user_data.deleted_count == 0:
            raise CustomException("User not found", 404)
        return True

    def get_by_email(self, email: str) -> Return | None:
        user = self.users_collection.find_one({"email": email})
        return user if user else None
