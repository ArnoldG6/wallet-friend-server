"""
@author: "Miguel González Carvajal".
Github username: "Miguelgonz98".
Contact me via "mgonzalex236@gmail.com".
GPL-3.0 license ©2022
"""
from sqlalchemy.testing.plugin.plugin_base import logging

from wallet_friend_dao import DAO
from wallet_friend_entities.Entities import Movement
from wallet_friend_exceptions.HttpWalletFriendExceptions import NonExistentRecordException
from wallet_friend_exceptions.WalletFriendExceptions import SingletonObjectException


class MovementDAO(DAO):
    """
    DBHandler class  manages the mqd_db queries in order to use CRUD methods.
    """
    __movement_dao_singleton = None  # Singleton AccountDAO object

    @staticmethod
    def get_instance():
        """
        Returns:
            MovementDAO: the MovementDAO class singleton object.
        """
        if MovementDAO.__movement_dao_singleton is None:
            MovementDAO.__movement_dao_singleton = MovementDAO()
        return MovementDAO.__movement_dao_singleton

    def __init__(self):
        super().__init__()
        if MovementDAO.__movement_dao_singleton is not None:
            raise SingletonObjectException()
        else:
            MovementDAO.__movement_dao_singleton = self

    def list_all(self):
        try:
            session = self.create_session()
            result = session.query(Movement).all()
            if result is None:
                raise NonExistentRecordException()
            return result
        except BaseException as e:
            logging.exception(f"DB Connection failed. Details: {e}")
            raise e

    def add(self, new_movement, username):
        try:
            session = self.create_session()
            #Pending to do
        except BaseException as e:
            logging.exception(f"DB Connection failed. Details: {e}")
            raise e

    def update(self, update_movement: Movement):
        try:
            session = self.create_session()
            filters = (Movement.id == update_movement.id)
            movement = session.query(Movement).filter(filters).one()
            if movement is None:
                raise NonExistentRecordException()
            else:
                movement.amount=update_movement.amount
                movement.available_amount = update_movement.available_amount
                movement.name = update_movement.name
                movement.description = update_movement.description
                #Pending updates
                session.commit()
        except BaseException as e:
            logging.exception(f"DB Connection failed. Details: {e}")
            raise e

    def delete(self, delete_account: Movement):
        try:
            session = self.create_session()
            filters = (Movement.id == delete_account.id)
            movement = session.query(Movement).filter(filters).one()
            if movement is None:
                raise NonExistentRecordException()
            else:
                session.delete(movement)
                session.commit()
        except BaseException as e:
            logging.exception(f"DB Connection failed. Details: {e}")
            raise e