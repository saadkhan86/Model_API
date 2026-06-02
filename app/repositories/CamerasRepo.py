from app.database.database import cameras_collection
from app.utils.to_object_id import to_object_id
from app.error_handler.custom_exception import CustomException
from app.schema.camera_schema import Return, Update, Create
from pymongo import ReturnDocument


class CamerasRepo:
    def __init__(self):
        self.cameras_collection = cameras_collection

    def create(self, data: Create) -> Return:
        camera_data = data.model_dump()
        camera_data["shop_id"] = to_object_id(camera_data["shop_id"])
        camera = self.cameras_collection.insert_one(camera_data)
        camera_data["_id"] = str(camera.inserted_id)
        return Return.model_validate(camera_data)

    def get(self, shop_id: str, camera_id: str) -> Return:
        camera_data = self.cameras_collection.find_one(
            {"_id": to_object_id(camera_id), "shop_id": to_object_id(shop_id)})
        if not camera_data:
            raise CustomException("camera not found", 404)
        return Return.model_validate(camera_data)

    def update(self, camera_id: str, data: Update) -> Return:
        camera = data.model_dump(exclude_unset=True)
        camera.pop("shop_id", None)
        camera_data = self.cameras_collection.find_one_and_update(
            {"_id": to_object_id(camera_id), "shop_id": to_object_id(
                data.shop_id)},
            {"$set": camera},
            return_document=ReturnDocument.AFTER
        )
        if not camera_data:
            raise CustomException(
                "camera not found or you do not have access", 404)
        return Return.model_validate(camera_data)

    def delete(self, shop_id: str, camera_id: str) -> bool:
        camera_data = self.cameras_collection.delete_one(
            {"_id": to_object_id(camera_id), "shop_id": to_object_id(shop_id)})
        if camera_data.deleted_count == 0:
            raise CustomException(
                "camera not found or you do not have access", 404)
        return True
