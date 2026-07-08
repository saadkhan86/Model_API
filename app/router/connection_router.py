from fastapi import APIRouter,status,Depends
from app.schema.connection_schema import Create,Response,Update
from app.middlewares.authenticate_user import get_current_user
import app.controller.connection_controller as connection_controller
connection_router = APIRouter(prefix="/connection",tags=["Connection"])

@connection_router.patch("/{shop_id}/{connection_id}",status_code=status.HTTP_200_OK,response_model=Response)
def update(shop_id:str,data:Update,connection_id:str,user_id=Depends(get_current_user)):
    connection = connection_controller.Update(user_id,shop_id,connection_id,data)
    return {"status":200,"success":True,"message":"connection updated successfully","data":connection}
@connection_router.get("/{shop_id}",status_code=status.HTTP_200_OK,response_model=Response)
def get(shop_id:str,user_id=Depends(get_current_user)):
    connection = connection_controller.Get(user_id,shop_id)
    return {"status":200,"success":True,"message":"connection fetched successfully","data":connection}
