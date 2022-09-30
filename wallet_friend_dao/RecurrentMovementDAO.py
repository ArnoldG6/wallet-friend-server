from wallet_friend_dao import DAO
from wallet_friend_exceptions.WalletFriendExceptions import SingletonObjectException


class RecurrentMovementDAO(DAO):
    """
    DBHandler class  manages the mqd_db queries in order to use CRUD methods.
    """
    __account_dao_singleton = None  # Singleton AccountDAO object

    @staticmethod
    def get_instance():
        """
        Returns:
            RecurrentMovementDAO: the RecurrentMovementDAO class singleton object.
        """
        if RecurrentMovementDAO.__account_dao_singleton is None:
            RecurrentMovementDAO.__account_dao_singleton = RecurrentMovementDAO()
        return RecurrentMovementDAO.__account_dao_singleton

    def __init__(self):
        super().__init__()
        if RecurrentMovementDAO.__account_dao_singleton is not None:
            raise SingletonObjectException()
        else:
            RecurrentMovementDAO.__account_dao_singleton = self