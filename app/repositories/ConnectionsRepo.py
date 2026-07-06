from app.config.database import connection_collection
from app.utils.to_object_id import to_object_id
from app.schema.connection_schema import Return , Create
from app.error_handler.custom_exception import CustomException
class ConnectionsRepo:
    def __init__(self):
        self.connection_collection = connection_collection
    
    def create(self, user_id:str , data:Create,session = None) -> Return:
        shop_data = data.model_dump()
        print(type(shop_data["shop_id"]))
        shop_data["shop_id"] = to_object_id(data.shop_id)
        print(type(shop_data["shop_id"]))
        inserted_connection = self.connection_collection.insert_one(shop_data,session=session)
        if not inserted_connection.inserted_id:
            raise CustomException("Connection not created(ConnectionsRepo.py)", 500)
        shop_data["_id"] = str(inserted_connection.inserted_id)
        return Return.model_validate(shop_data)
    def update(self, shop_id:str,connection_id:str , data:Create) -> Return:
        shop_data = self.connection_collection.find_one_and_update({
            "_id":to_object_id(connection_id),
            "shop_id":to_object_id(shop_id)
        },{"$set":data.model_dump(exclude_unset=True)})  
        if not shop_data:
            raise CustomException("Connection not found (ConnectionsRepo)", 404)
        return Return.model_validate(shop_data)
    def get(self, shop_id:str) -> Return:
        shop_data = self.connection_collection.find_one({
            "shop_id":to_object_id(shop_id)
        })
        if not shop_data:
            raise CustomException("Connection not found (ConnectionsRepo)", 404)
        print(shop_data)
        return Return.model_validate(shop_data)
    

        
