"""
@author: "Miguel González Carvajal".
Github username: "Miguelgonz98".
Contact me via "mgonzalex236@gmail.com".
GPL-3.0 license ©2022
"""
import datetime
import logging

from sqlalchemy.exc import NoResultFound

from .DAO import DAO
from wallet_friend_entities.Entities import Bag, Account, BagMovement
from wallet_friend_exceptions.HttpWalletFriendExceptions import NonExistentRecordException, MalformedRequestException, \
    ExistentRecordException
from wallet_friend_exceptions.WalletFriendExceptions import SingletonObjectException


class BagDAO(DAO):
    """
    DBHandler class  manages the mqd_db queries in order to use CRUD methods.
    """
    __bag_dao_singleton = None  # Singleton AccountDAO object

    @staticmethod
    def get_instance():
        """
        Returns:
            BagDAO: the BagDAO class singleton object.
        """
        if BagDAO.__bag_dao_singleton is None:
            BagDAO.__bag_dao_singleton = BagDAO()
        return BagDAO.__bag_dao_singleton

    def __init__(self):
        super().__init__()
        if BagDAO.__bag_dao_singleton is not None:
            raise SingletonObjectException()
        else:
            BagDAO.__bag_dao_singleton = self

    def list_all(self):
        try:
            session = self.create_session()
            result = session.query(Bag).all()
            if result is None:
                raise NonExistentRecordException()
            return result
        except BaseException as e:
            logging.exception(f"DB Connection failed. Details: {e}")
            raise e

    def add(self, new_bag: Bag):
        session = None
        try:
            if not new_bag:
                raise MalformedRequestException("Invalid parameter 'new_bag' exception")
            session = self.create_session()
            account = None
            account_id = new_bag.account_id
            new_bag.name = new_bag.name.title()
            try:
                if session.query(Bag).filter(Bag.name == new_bag.name).one():
                    raise ExistentRecordException(f"Bag name '{new_bag.name}' already exists")
            except NoResultFound:
                pass
            try:
                account = session.query(Account).filter(Account.id == account_id).one()
            except NoResultFound as e:
                raise NonExistentRecordException("Account does not exists")
            new_bag.account = account
            new_bag.account_id = account.id
            new_bag.creation_datetime = datetime.datetime.now()
            new_bag.done = False
            new_bag.balance = 0
            session.add(new_bag)
            session.commit()
        except ExistentRecordException as e:
            logging.exception(e)
            raise e
        except BaseException as e:  # Any other Exception
            logging.exception(f"DB Connection failed. Details: {e}")
            raise e
        finally:
            if session:
                session.close()

    def update(self, update_bag: Bag):
        try:
            session = self.create_session()
            filters = (Bag.id == update_bag.id)
            bag = session.query(Bag).filter(filters).one()
            if bag is None:
                raise NonExistentRecordException()
            else:
                bag.balance = update_bag.balance
                bag.goal_balance = update_bag.goal_balance
                bag.done = update_bag.done
                # Pending updates
                session.commit()
        except BaseException as e:
            logging.exception(f"DB Connection failed. Details: {e}")
            raise e

    def delete(self, bag_to_delete_id: int):
        try:
            bag_to_delete = None
            session = self.create_session()
            try:
                bag_to_delete = session.query(Bag).filter((Bag.id == bag_to_delete_id)).one()
            except NoResultFound as e:
                raise NonExistentRecordException(f"Bag with id '{bag_to_delete_id}' does not exists.")
            session.delete(bag_to_delete)
            session.commit()
        except BaseException as e:
            logging.exception(f"DB Connection failed. Details: {e}")
            raise e

    def delete_bag_movement_from_bag(self, bag_movement_id: int):
        try:
            bag_movement_to_delete = None
            session = self.create_session()
            try:
                bag_movement_to_delete = session.query(BagMovement).filter((BagMovement.id == bag_movement_id)).one()
            except NoResultFound as e:
                raise NonExistentRecordException(f"BagMovement with id '{bag_movement_id}' does not exists.")
            session.delete(bag_movement_to_delete)
            session.commit()
        except BaseException as e:
            logging.exception(f"DB Connection failed. Details: {e}")
            raise e
