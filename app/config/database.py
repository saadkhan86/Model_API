from pymongo import MongoClient
from app.config.environment_config import environment
mongo_client = MongoClient(environment.MONGO_DB_URI)
db = mongo_client["Veesion"]

users_collection = db["users"]
shops_collection = db["shops"]
cameras_collection = db["cameras"]
connection_collection= db["connections"]

def init_db():
    users_collection.create_index([("email", 1)], unique=True)
    shops_collection.create_index([("name",1),("branch_name",1),("city",1),("country",1)],unique=True)
    connection_collection.create_index([("shop_id",1)],unique=True)
    cameras_collection.create_index([("channel_no",1),("shop_id",1)],unique=True)
