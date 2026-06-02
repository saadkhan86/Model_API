from app.schema.shop_schema import Return, Update, Create
from app.repositories.ShopsRepo import ShopsRepo
from app.utils.error_wrapper import error_wrapper


shops_repo = ShopsRepo()


@error_wrapper
def create(user_id: str, data: Create):
    return shops_repo.create(user_id, data)


@error_wrapper
def update(user_id, shop_id, data: Update):
    return shops_repo.update(user_id, shop_id, data)


@error_wrapper
def get(user_id, shop_id):
    return shops_repo.get(user_id, shop_id)


@error_wrapper
def delete(user_id, shop_id):
    return shops_repo.delete(user_id, shop_id)
