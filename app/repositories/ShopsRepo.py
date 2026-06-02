from app.error_handler.custom_exception import CustomException
from pymongo import ReturnDocument
from app.utils.to_object_id import to_object_id
from app.config.database import shops_collection
from app.schema.shop_schema import Create, Return, Update


class ShopsRepo:
    def __init__(self):
        self.shops_collection = shops_collection

    def create(self, user_id: str, data: Create) -> Return:
        shop_data = data.model_dump()
        shop_data["user_id"] = to_object_id(user_id)
        inserted_shop = self.shops_collection.insert_one(shop_data)
        if not inserted_shop.inserted_id:
            raise CustomException("shop not created", 500)
        shop_data["_id"] = str(inserted_shop.inserted_id)
        return Return.model_validate(shop_data)

    def update(self, user_id: str, shop_id: str, data: Update) -> Return:
        shop_data = self.shops_collection.find_one_and_update(
            {
                "_id": to_object_id(shop_id),
                "user_id": to_object_id(user_id)
            },
            {
                "$set": data.model_dump(exclude_unset=True)
            }, return_document=ReturnDocument.AFTER
        )
        if not shop_data:
            raise CustomException("Shop not found or access denied", 404)
        return Return.model_validate(shop_data)

    def get(self, user_id: str, shop_id: str) -> Return:
        shop_data = self.shops_collection.find_one(
            {
                "_id": to_object_id(shop_id),
                "user_id": to_object_id(user_id)
            }
        )
        if not shop_data:
            raise CustomException("shop not found", 404)
        return Return.model_validate(shop_data)

    def delete(self, user_id: str, shop_id: str) -> bool:
        shop_data = self.shops_collection.delete_one(
            {
                "_id": to_object_id(shop_id),
                "user_id": to_object_id(user_id)
            }
        )
        if shop_data.deleted_count == 0:
            raise CustomException("Shop not found or access denied", 404)
        return True
