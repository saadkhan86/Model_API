from app.database.database import db
from bson import ObjectId

shops_collection = db["shops"]


def to_object_id(id: str):
    return ObjectId(id)


def create_shop(shop: dict):
    return shops_collection.insert_one(shop)


def update_shop(shop_id: str, user_id: str, shop: dict):
    return shops_collection.update_one(
        {
            "_id": to_object_id(shop_id),
            "user_id": to_object_id(user_id)
        },
        {
            "$set": shop
        }
    )


def get_shop_by_id(shop_id: str, user_id: str):
    return shops_collection.find_one(
        {
            "_id": to_object_id(shop_id),
            "user_id": to_object_id(user_id)
        }
    )


def delete_shop(shop_id: str, user_id: str):
    return shops_collection.delete_one(
        {
            "_id": to_object_id(shop_id),
            "user_id": to_object_id(user_id)
        }
    )


def query_shops(data: dict):
    return list(shops_collection.find(data))
