from bson.objectid import ObjectId
from app.error_handler.custom_exception import CustomException


def to_object_id(id: str):
    try:
        return ObjectId(id)
    except Exception as e:
        raise CustomException("Invalid id format", 400)
