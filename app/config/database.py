from pymongo import MongoClient
from app.config.environment_config import environment
mongo_client = MongoClient(environment.MONGO_DB_URI)
db = mongo_client["AIAssist"]

users_collection = db["users"]
shops_collection = db["shops"]
cameras_collection = db["cameras"]


def init_db():
    users_collection.create_index([("email", 1)], unique=True)
    cameras_collection.create_index([("port", 1)], unique=True)
