"""
@author: "Miguel González Carvajal".
Github username: "Miguelgonz98".
Contact me via "mgonzalex236@gmail.com".
GPL-3.0 license ©2022
"""
from .DAO import DAO
from wallet_friend_entities.Entities import Movement
from wallet_friend_exceptions.WalletFriendExceptions import SingletonObjectException


class FixedMovementDAO(DAO):
    """
    DBHandler class  manages the mqd_db queries in order to use CRUD methods.
    """
    __fixed_movement_dao_singleton = None  # Singleton FixedMovementDAO object

    @staticmethod
    def get_instance():
        """
        Returns:
            FixedMovementDAO: the FixedMovementDAO class singleton object.
        """
        if FixedMovementDAO.__fixed_movement_dao_singleton is None:
            FixedMovementDAO.__fixed_movement_dao_singleton = FixedMovementDAO()
        return FixedMovementDAO.__fixed_movement_dao_singleton

    def __init__(self):
        super().__init__()
        if FixedMovementDAO.__fixed_movement_dao_singleton is not None:
            raise SingletonObjectException()
        else:
            FixedMovementDAO.__fixed_movement_dao_singleton = self

    def add(self, fixed_movement: Movement):
        pass
