"""
@author: "Miguel González Carvajal".
Github username: "Miguelgonz98".
Contact me via "mgonzalex236@gmail.com".
GPL-3.0 license ©2022
"""
import logging

from .DAO import DAO
from wallet_friend_entities.Entities import Bag
from wallet_friend_exceptions.HttpWalletFriendExceptions import NonExistentRecordException
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
        try:
            session = self.create_session()
            #Pending to do
        except BaseException as e:
            logging.exception(f"DB Connection failed. Details: {e}")
            raise e

    def update(self, update_bag: Bag):
        try:
            session = self.create_session()
            filters = (Bag.id == update_bag.id)
            bag = session.query(Bag).filter(filters).one()
            if bag is None:
                raise NonExistentRecordException()
            else:
                bag.balance=update_bag.balance
                bag.goal_balance=update_bag.goal_balance
                bag.done=update_bag.done
                #Pending updates
                session.commit()
        except BaseException as e:
            logging.exception(f"DB Connection failed. Details: {e}")
            raise e

    def delete(self, delete_bag: Bag):
        try:
            session = self.create_session()
            filters = (Bag.id == delete_bag.id)
            bag = session.query(Bag).filter(filters).one()
            if bag is None:
                raise NonExistentRecordException()
            else:
                session.delete(bag)
                session.commit()
        except BaseException as e:
            logging.exception(f"DB Connection failed. Details: {e}")
            raise e

