from pymongo import MongoClient
from app.schema.user_schema import UserSignUpSchema
from app.schema.shop_schema import ShopCreateSchema
mongo_client = MongoClient("mongodb://localhost:27017/")
db = mongo_client["AIAssist"]

users_collection = db["users"]
shops_collection = db["shops"]
cameras_collection = db["cameras"]


def init_db():
    users_collection.create_index([("email", 1)], unique=True)
