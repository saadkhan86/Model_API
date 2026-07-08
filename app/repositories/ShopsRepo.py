from app.error_handler.custom_exception import CustomException
from pymongo import ReturnDocument
from app.utils.to_object_id import to_object_id
from app.config.database import shops_collection
from app.schema.shop_schema import Create, Return, Update , ListResponse
class ShopsRepo:
    def __init__(self):
        self.shops_collection = shops_collection

    def create(self, user_id: str, data: Create,session = None) -> Return:
        shop_data = data.model_dump()
        shop_data["owner_id"] = to_object_id(user_id)
        inserted_shop = self.shops_collection.insert_one(shop_data,session=session)
        if not inserted_shop.inserted_id:
            raise CustomException("shop not created (ShopsRepo.py)", 500)
        shop_data["_id"] = str(inserted_shop.inserted_id)
        return Return.model_validate(shop_data)
    
    def get_all(self,user_id:str) -> ListResponse:
        shops = self.shops_collection.find({"owner_id": to_object_id(user_id), "soft_delete": False})
        return [Return.model_validate(shop) for shop in shops]
        
    
    def update(self, user_id: str, shop_id: str, data: Update) -> Return:
        shop_data = self.shops_collection.find_one_and_update(
            {
                "_id": to_object_id(shop_id),
                "user_id": to_object_id(user_id),
                "soft_delete": False
            },
            {
                "$set": data.model_dump(exclude_unset=True)
            }, return_document=ReturnDocument.AFTER
        )
        if not shop_data:
            raise CustomException("Shop not found or access denied (ShopsRepo.py)", 404)
        return Return.model_validate(shop_data)

    def get(self, user_id: str, shop_id: str) -> Return:
        shop_data = self.shops_collection.find_one(
            {
                "_id": to_object_id(shop_id),
                "owner_id": to_object_id(user_id),
                "soft_delete": False
            }
        )
        if not shop_data:
            raise CustomException("shop not found (ShopsRepo.py)", 404)
        return Return.model_validate(shop_data)

    def delete(self, user_id: str, shop_id: str) -> bool:
        shop_data = self.shops_collection.find_one_and_update(
            {
                "_id": to_object_id(shop_id),
                "owner_id": to_object_id(user_id),
                "soft_delete": False
            },
            {
                "$set": {"soft_delete": True}
            }
        )
        if not shop_data:
            raise CustomException("Shop not found or access denied (ShopsRepo.py)", 404)
        return True
