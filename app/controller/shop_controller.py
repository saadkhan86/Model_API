from app.schema.shop_schema import ShopCreateSchema, ShopResponseSchema, ShopUpdateSchema
from app.repositories.ShopsRepo import ShopsRepo
from app.utils.error_wrapper import error_wrapper


shops_repo = ShopsRepo()


@error_wrapper
def create_shop(user_id: str, data: ShopCreateSchema):
    return shops_repo.create_shop(user_id, data)


@error_wrapper
def update_shop(user_id, shop_id, shop: ShopUpdateSchema):
    return shops_repo.update_shop(user_id, shop_id, shop)


@error_wrapper
def get_shop(user_id, shop_id):
    return shops_repo.get_shop(user_id, shop_id)


@error_wrapper
def delete_shop(user_id, shop_id):
    return shops_repo.delete_shop(user_id, shop_id)
