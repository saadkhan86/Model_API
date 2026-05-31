from app.schema.shop_schema import ShopCreateSchema, ShopResponseSchema, ShopUpdateSchema
from app.models import shops_model
from fastapi import HTTPException, status


def create_shop(user_id: str, shop: ShopCreateSchema):
    inserted_shop = shops_model.create_shop(user_id, shop.model_dump())
    print(inserted_shop)
    return inserted_shop


def update_shop(user_id, shop_id, shop: ShopUpdateSchema):
    updated_shop = shops_model.update_shop(user_id, shop_id, shop.model_dump())
    if not updated_shop:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Shop not found or access denied")
    return updated_shop


def get_shop_by_id(user_id, shop_id):
    shop = shops_model.get_shop_by_id(user_id, shop_id)
    if not shop:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Shop not found")
    return shop


def delete_shop_by_id(user_id, shop_id):
    shop = shops_model.delete_shop_by_id(user_id, shop_id)
    if not shop:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Shop not found or access denied")
    return shop
