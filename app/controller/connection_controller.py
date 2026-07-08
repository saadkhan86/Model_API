from app.utils.error_wrapper import error_wrapper
from app.error_handler.custom_exception import CustomException
from app.schema.connection_schema import Create,Update,Response
from app.repositories.ShopsRepo import ShopsRepo
from app.repositories.ConnectionsRepo import ConnectionsRepo
connection_repo = ConnectionsRepo()
shops_repo = ShopsRepo()

@error_wrapper
def Update(user_id:str , shop_id:str , connection_id:str,data:Update):
    if not shops_repo.get(user_id,shop_id):
        raise CustomException("shop does not exists(connection_controller)",404)
    connection = connection_repo.update(shop_id,connection_id,data)
    return connection


@error_wrapper
def Get(user_id:str,shop_id:str):
    if not shops_repo.get(user_id,shop_id):
        raise CustomException("shop does not exists(connection_controller)",404)
    connection = connection_repo.get(shop_id)
    return connection
