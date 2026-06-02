from app.utils.error_wrapper import error_wrapper
from app.repositories.CamerasRepo import CamerasRepo
from app.schema.camera_schema import Create, Update
from app.repositories.ShopsRepo import ShopsRepo

camera_repo = CamerasRepo()
shops_repo = ShopsRepo()


@error_wrapper
def create(data: Create, user_id):
    shops_repo.get(user_id, data.shop_id)
    return camera_repo.create(data)


@error_wrapper
def get(shop_id: str, camera_id: str, user_id: str):
    shops_repo.get(user_id, shop_id)
    return camera_repo.get(shop_id, camera_id)


@error_wrapper
def update(camera_id: str, data: Update, user_id: str):
    shops_repo.get(user_id, str(data.shop_id))
    return camera_repo.update(camera_id, data)


@error_wrapper
def delete(shop_id: str, camera_id: str, user_id: str):
    shops_repo.get(user_id, shop_id)
    return camera_repo.delete(shop_id, camera_id)
