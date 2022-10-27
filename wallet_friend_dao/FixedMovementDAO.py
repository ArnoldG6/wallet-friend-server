"""
@author: "Miguel González Carvajal".
Github username: "Miguelgonz98".
Contact me via "mgonzalex236@gmail.com".
GPL-3.0 license ©2022
"""
import datetime
import logging

from sqlalchemy.exc import NoResultFound

from wallet_friend_exceptions.HttpWalletFriendExceptions import MalformedRequestException, NonExistentRecordException, \
    ExistentRecordException
from .DAO import DAO
from wallet_friend_entities.Entities import Movement, FixedMovement, Account
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

    def add(self, new_fixed_movement: FixedMovement):
        session = None
        a = None
        try:
            if not new_fixed_movement:
                raise MalformedRequestException("Invalid parameter 'new_movement' exception")
            account_id = new_fixed_movement.account_id
            session = self.create_session()
            try:
                a = session.query(Account).filter(Account.id == account_id).one()
            except NoResultFound as e:
                raise NonExistentRecordException("This record is not existent")
            new_fixed_movement.account_id = account_id
            new_fixed_movement.creation_datetime = datetime.datetime.now()
            session.add(new_fixed_movement)
            session.commit()
        except ExistentRecordException as e:
            logging.exception(e)
            raise e
        except Exception as e:  # Any other Exception
            logging.exception(f"DB Connection failed. Details: {e}")
            raise e
        finally:
            if session:
                session.close()
