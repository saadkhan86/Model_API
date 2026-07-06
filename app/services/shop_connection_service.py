from app.config.database import mongo_client as client
from app.repositories.ShopsRepo import ShopsRepo
from app.repositories.ConnectionsRepo import ConnectionsRepo
from app.schema.connection_schema import Create as CreateConnection
from app.error_handler.custom_exception import CustomException

class ShopConnectionService:
    def __init__(self):
        self.shop_repo = ShopsRepo()
        self.connection_repo = ConnectionsRepo()

    def create(self,user_id, data):

        try:

            with client.start_session() as session:
                with session.start_transaction():

                    shop = self.shop_repo.create(
                        user_id=user_id,
                        data=data,
                        session=session,
                    )

                    self.connection_repo.create(
                        user_id=user_id,
                        data=CreateConnection(
                            shop_id=shop.id,
                            status="disconnected",
                            is_active=False,
                            soft_delete=False
                        ),
                        session=session,
                    )

                    return shop

        except CustomException:
            raise

        except Exception as e:
            raise CustomException(
                f"{self.__class__.__name__}.create() failed : {str(e)}",
                500
            )