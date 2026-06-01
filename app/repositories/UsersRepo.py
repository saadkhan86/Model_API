from app.schema.user_schema import UserSignUpSchema, UserLoginSchema, UserResponseSchema, UserUpdateSchema
from app.database.database import users_collection
from app.error_handler.custom_exception import CustomException
from pymongo import ReturnDocument
from app.utils.to_object_id import to_object_id


class UsersRepo:
    def __init__(self):
        self.users_collection = users_collection

    def create_user(self, data: UserSignUpSchema) -> UserResponseSchema:
        user_data = data.model_dump(exclude_unset=True)
        inserted_user = self.users_collection.insert_one(user_data)
        if not inserted_user.inserted_id:
            raise CustomException("User not created", 500)
        user_data["_id"] = str(inserted_user.inserted_id)
        return UserResponseSchema.model_validate(user_data)

    def get_user_by_id(self, user_id: str) -> UserResponseSchema:
        user_data = self.users_collection.find_one(
            {"_id": to_object_id(user_id)})
        if not user_data:
            raise CustomException("User not found", 404)
        return UserResponseSchema.model_validate(user_data)

    def update_user(self, user_id: str, data: UserUpdateSchema) -> UserResponseSchema:
        new_data = data.model_dump(exclude_unset=True)
        user_data = self.users_collection.find_one_and_update({"_id": to_object_id(user_id)}, {
            "$set": new_data}, return_document=ReturnDocument.AFTER)
        if not user_data:
            raise CustomException(f"User not found for ID : {user_id}", 404)
        return UserResponseSchema.model_validate(user_data)

    def delete_user(self, user_id: str) -> bool:
        user_data = self.users_collection.delete_one(
            {"_id": to_object_id(user_id)})
        if user_data.deleted_count == 0:
            raise CustomException("User not found", 404)
        return True

    def get_user_by_email(self, email: str) -> UserResponseSchema | None:
        user = self.users_collection.find_one({"email": email})
        return user if user else None
