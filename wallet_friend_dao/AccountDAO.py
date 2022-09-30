"""
@author: "Miguel González Carvajal".
Github username: "Miguelgonz98".
Contact me via "mgonzalex236@gmail.com".
GPL-3.0 license ©2022
"""
from sqlalchemy.testing.plugin.plugin_base import logging

from wallet_friend_dao import DAO
from wallet_friend_entities.Entities import Account
from wallet_friend_exceptions.HttpWalletFriendExceptions import NonExistentRecordException
from wallet_friend_exceptions.WalletFriendExceptions import SingletonObjectException


class AccountDAO(DAO):
    """
    DBHandler class  manages the mqd_db queries in order to use CRUD methods.
    """
    __account_dao_singleton = None  # Singleton AccountDAO object

    @staticmethod
    def get_instance():
        """
        Returns:
            AccountDAO: the AccountDAO class singleton object.
        """
        if AccountDAO.__account_dao_singleton is None:
            AccountDAO.__account_dao_singleton = AccountDAO()
        return AccountDAO.__account_dao_singleton

    def __init__(self):
        super().__init__()
        if AccountDAO.__account_dao_singleton is not None:
            raise SingletonObjectException()
        else:
            AccountDAO.__account_dao_singleton = self

    def list_all(self):
        try:
            session = self.create_session()
            result = session.query(Account).all()
            if result is None:
                raise NonExistentRecordException()
            return result
        except BaseException as e:
            logging.exception(f"DB Connection failed. Details: {e}")
            raise e

    def add(self, new_account: Account):
        try:
            session = self.create_session()
            #Pending to do
        except BaseException as e:
            logging.exception(f"DB Connection failed. Details: {e}")
            raise e

    def update(self, update_account: Account):
        try:
            session = self.create_session()
            filters = (Account.id == update_account.id)
            account = session.query(Account).filter(filters).one()
            if account is None:
                raise NonExistentRecordException()
            else:
                account.total_balance=update_account.total_balance
                #Pending updates
                session.commit()
        except BaseException as e:
            logging.exception(f"DB Connection failed. Details: {e}")
            raise e

    def delete(self, delete_account: Account):
        try:
            session = self.create_session()
            filters = (Account.id == delete_account.id)
            account = session.query(Account).filter(filters).one()
            if account is None:
                raise NonExistentRecordException()
            else:
                session.delete(account)
                session.commit()
        except BaseException as e:
            logging.exception(f"DB Connection failed. Details: {e}")
            raise e