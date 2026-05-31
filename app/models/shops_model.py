from app.database.database import db
from bson import ObjectId
from pymongo import ReturnDocument
shops_collection = db["shops"]


def to_object_id(id: str):
    return ObjectId(id)


def create_shop(user_id: str, shop: dict):
    shop["user_id"] = to_object_id(user_id)
    result = shops_collection.insert_one(shop)
    shop["_id"] = str(result.inserted_id)
    shop["user_id"] = str(shop["user_id"])
    return shop


def update_shop(user_id: str, shop_id: str, shop: dict):
    updated_shop = shops_collection.find_one_and_update(
        {
            "_id": to_object_id(shop_id),
            "user_id": to_object_id(user_id)
        },
        {
            "$set": shop
        }, return_document=ReturnDocument.AFTER
    )
    if (updated_shop):
        updated_shop["_id"] = str(updated_shop["_id"])
        updated_shop["user_id"] = str(updated_shop["user_id"])
    return updated_shop


def get_shop_by_id(user_id: str, shop_id: str):
    shop = shops_collection.find_one(
        {
            "_id": to_object_id(shop_id),
            "user_id": to_object_id(user_id)
        }
    )
    return shop


def delete_shop(shop_id: str, user_id: str):
    shop = shops_collection.delete_one(
        {
            "_id": to_object_id(shop_id),
            "user_id": to_object_id(user_id)
        }
    )
    return shop.deleted_count > 0


def query_shops(data: dict):
    return list(shops_collection.find(data))
