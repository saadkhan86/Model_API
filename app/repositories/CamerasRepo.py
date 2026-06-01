from app.database.database import cameras_collection
from app.utils.to_object_id import to_object_id
from app.error_handler.custom_exception import CustomException
from app.schema.camera_schema import CameraResponseSchema, CameraUpdateSchema, CameraCreateSchema
from pymongo import ReturnDocument


class CamerasRepo:
    def __init__(self):
        self.cameras_collection = cameras_collection

    def create_camera(self, data: CameraCreateSchema) -> CameraResponseSchema:
        camera_data = data.model_dump()
        camera_data["shop_id"] = to_object_id(camera_data["shop_id"])
        camera = self.cameras_collection.insert_one(camera_data)
        camera_data["_id"] = str(camera.inserted_id)
        return CameraResponseSchema.model_validate(camera_data)

    def get_camera(self, shop_id: str, camera_id: str) -> CameraResponseSchema:
        camera = self.cameras_collection.find_one(
            {"_id": to_object_id(camera_id), "shop_id": to_object_id(shop_id)})
        if not camera:
            raise CustomException("camera not found", 404)
        return CameraResponseSchema.model_validate(camera)

    def update_camera(self, camera_id: str, camera_data: CameraUpdateSchema) -> CameraResponseSchema:
        result = self.cameras_collection.find_one_and_update(
            {"_id": to_object_id(camera_id), "shop_id": to_object_id(
                camera_data.shop_id)},
            {"$set": camera_data.model_dump(exclude_unset=True)},
            return_document=ReturnDocument.AFTER
        )
        if not result:
            raise CustomException(
                "camera not found or you do not have access", 404)
        return CameraResponseSchema.model_validate(result)

    def delete_camera(self, shop_id: str, camera_id: str) -> bool:
        result = self.cameras_collection.delete_one(
            {"_id": to_object_id(camera_id), "shop_id": to_object_id(shop_id)})
        if result.deleted_count == 0:
            raise CustomException(
                "camera not found or you do not have access", 404)
        return True
