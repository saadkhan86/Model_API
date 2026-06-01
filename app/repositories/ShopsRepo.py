from app.error_handler.custom_exception import CustomException
from pymongo import ReturnDocument
from app.utils.to_object_id import to_object_id
from app.database.database import shops_collection
from app.schema.shop_schema import ShopCreateSchema, ShopResponseSchema, ShopUpdateSchema


class ShopsRepo:
    def __init__(self):
        self.shops_collection = shops_collection

    def create_shop(self, user_id: str, shop: ShopCreateSchema):
        shop_dict = shop.model_dump()
        shop_dict["user_id"] = to_object_id(user_id)
        inserted_shop = self.shops_collection.insert_one(shop_dict)
        if not inserted_shop.inserted_id:
            raise CustomException("shop not created", 500)
        shop_dict["_id"] = str(inserted_shop.inserted_id)
        return ShopResponseSchema.model_validate(shop_dict)

    def update_shop(self, user_id: str, shop_id: str, shop: ShopUpdateSchema):
        shop_dict = shop.model_dump(exclude_unset=True)
        updated_shop = self.shops_collection.find_one_and_update(
            {
                "_id": to_object_id(shop_id),
                "user_id": to_object_id(user_id)
            },
            {
                "$set": shop_dict
            }, return_document=ReturnDocument.AFTER
        )
        if not updated_shop:
            raise CustomException("Shop not found or access denied", 404)
        return ShopResponseSchema.model_validate(updated_shop)

    def get_shop(self, user_id: str, shop_id: str):
        shop = self.shops_collection.find_one(
            {
                "_id": to_object_id(shop_id),
                "user_id": to_object_id(user_id)
            }
        )
        if not shop:
            raise CustomException("shop not found", 404)
        return ShopResponseSchema.model_validate(shop)

    def delete_shop(self, user_id: str, shop_id: str):
        shop = self.shops_collection.delete_one(
            {
                "_id": to_object_id(shop_id),
                "user_id": to_object_id(user_id)
            }
        )
        if shop.deleted_count == 0:
            raise CustomException("Shop not found or access denied", 404)
        return True
