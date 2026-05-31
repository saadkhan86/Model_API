from pymongo import MongoClient
from app.schema.user_schema import UserSignUpSchema
mongo_client = MongoClient("mongodb://localhost:27017/")
db = mongo_client["AIAssist"]

users_collection = db["users"]
shops_collection = db["shops"]


def init_db():
    users_collection.create_index([("email", 1)], unique=True)
    db.command("collMod", "users", validator={
        "$jsonSchema": UserSignUpSchema.model_json_schema()
    })
