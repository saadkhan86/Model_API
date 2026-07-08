from app.schema.shop_schema import Return, Update, Create
from app.repositories.ShopsRepo import ShopsRepo
from app.utils.error_wrapper import error_wrapper
from app.services.shop_connection_service import ShopConnectionService
shop_connection_service = ShopConnectionService()
shops_repo = ShopsRepo()


@error_wrapper
def create(user_id: str, data: Create):
    return shop_connection_service.create(user_id, data)

@error_wrapper
def get_all(user_id: str):
    return shops_repo.get_all(user_id)

@error_wrapper
def update(user_id, shop_id, data: Update):
    return shops_repo.update(user_id, shop_id, data)


@error_wrapper
def get(user_id, shop_id):
    return shops_repo.get(user_id, shop_id)


@error_wrapper
def delete(user_id, shop_id):
    return shops_repo.delete(user_id, shop_id)
