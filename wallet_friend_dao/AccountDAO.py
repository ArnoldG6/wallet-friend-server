"""
@author: "Miguel González Carvajal".
Github username: "Miguelgonz98".
Contact me via "mgonzalex236@gmail.com".
GPL-3.0 license ©2022
"""
from __future__ import annotations
import datetime

from sqlalchemy.exc import NoResultFound
from sqlalchemy.testing.plugin.plugin_base import logging

from wallet_friend_exceptions.WalletFriendExceptions import SingletonObjectException
from wallet_friend_settings import default_db_settings_path
from .DAO import DAO
from wallet_friend_entities.Entities import Account, User
from wallet_friend_exceptions.HttpWalletFriendExceptions import NonExistentRecordException, MalformedRequestException, \
    ExistentRecordException


class AccountDAO(DAO):
    """
    DBHandler class  manages the mqd_db queries in order to use CRUD methods.
    """
    __account_dao_singleton = None  # Singleton AccountDAO object

    @staticmethod
    def get_instance(path=default_db_settings_path()) -> AccountDAO:
        """
        Returns:
            AccountDAO: the AccountDAO class singleton object.
        """
        if AccountDAO.__account_dao_singleton is None:
            AccountDAO.__account_dao_singleton = AccountDAO(path)
        return AccountDAO.__account_dao_singleton

    def __init__(self, path=default_db_settings_path()):
        super().__init__(path)
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

    def add(self, new_account: Account, owner_username: str):
        session = None
        u = None
        try:
            if not new_account:
                raise MalformedRequestException("Invalid parameter 'new_account' exception")
            session = self.create_session()
            try:
                u = session.query(User).filter(User.username == owner_username).one()
            except NoResultFound as e:
                raise NonExistentRecordException("This record is not existent")
            new_account.owner = u
            new_account.owner_id = u.id
            new_account.creation_datetime = datetime.datetime.now()
            new_account.movements = []
            new_account.fixed_movements = []
            new_account.bags = []
            session.add(new_account)
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

    def update(self, update_account: Account):
        try:
            session = self.create_session()
            filters = (Account.id == update_account.id)
            account = session.query(Account).filter(filters).one()
            if account is None:
                raise NonExistentRecordException()
            else:
                account.total_balance = update_account.total_balance
                # Pending updates
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

    def search_account_by_id(self, account_id: int):
        """
        Parameters:
            param id: id to search account.
        Returns:
            Account: Existing account.
        """
        session = None
        try:
            session = self.create_session()
            filters = (Account.id == account_id)
            account_result = session.query(User).filter(filters).one()
            if not account_result:
                raise NonExistentRecordException()
            return account_result
        except Exception as e:
            logging.exception(f"DB Connection failed. Details: {e}")
            raise e
        finally:
            if session:
                session.close()