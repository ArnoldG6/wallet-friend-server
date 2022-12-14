"""
@author: "Arnoldo J. González Quesada".
Github username: "ArnoldG6".
Contact me via "arnoldgq612@gmail.com".
GPL-3.0 license ©2022
"""
from __future__ import annotations

import datetime
import hashlib
import logging
import re
import time

import jwt
from sqlalchemy.exc import NoResultFound

from wallet_friend_dto import UserAuthDTO
from wallet_friend_entities import User
from wallet_friend_entities.Entities import Account
from wallet_friend_exceptions.HttpWalletFriendExceptions import NotAuthorizedException, DisabledUserException, \
    MalformedRequestException, ExistentRecordException, NonExistentRecordException
from wallet_friend_exceptions.WalletFriendExceptions import SingletonObjectException
from wallet_friend_mappers.AccountMapper import AccountMapper
from wallet_friend_mappers.UserMapper import UserMapper
from wallet_friend_settings import default_password_pattern, default_db_settings_path
from wallet_friend_tools import check_non_empty_non_spaces_string
from . import RoleDAO
from .DAO import DAO


class UserDAO(DAO):
    """
    UserDAO class  manages db queries in order to use CRUD methods.
    """
    __user_dao_singleton = None  # Singleton UserDAO object

    @staticmethod
    def get_instance(path=default_db_settings_path()) -> UserDAO:
        """
        Returns:
            UserDAO: the UserDAO class singleton object.
        """
        if not UserDAO.__user_dao_singleton:
            UserDAO.__user_dao_singleton = UserDAO(path)
        return UserDAO.__user_dao_singleton

    def __init__(self, path=default_db_settings_path()):
        super().__init__(path)
        if UserDAO.__user_dao_singleton:
            raise SingletonObjectException()
        else:
            UserDAO.__user_dao_singleton = self

    def auth_user(self, user_auth_dto: UserAuthDTO, secret_key: str) -> dict or None:
        """
        Parameters:
            param secret_key: key used to generate the JWT along the payload.
            param user_auth_dto:  Valid DTO Input data.
        Returns:
            dict: an authorized User object.
                {
                    "user:" User,
                    "access_token": access_token
                }
            None: If auth operation fails.
        """
        session = None
        username = user_auth_dto.username
        pwd = user_auth_dto.password
        try:
            if not check_non_empty_non_spaces_string(pwd):
                raise MalformedRequestException("Invalid parameter 'pwd' exception")
            if not check_non_empty_non_spaces_string(username):
                raise MalformedRequestException("Invalid parameter 'username' exception")
            if not check_non_empty_non_spaces_string(secret_key):
                raise MalformedRequestException("Invalid parameter 'secret_key' exception")
            session = self.create_session()
            logging.info(f"DB Connection requested by user: '{username}' is established.")
            try:
                filters = (((User.username == username) | (User.email == username)) & (User.pwd_hash == pwd))
                u = session.query(User).filter(filters).one()
                if not u:
                    raise NotAuthorizedException()
                if not u.enabled:  # If user is disabled.
                    raise DisabledUserException()
                if u.token:
                    return {
                        "access_token": u.token,
                        "user": UserMapper.get_instance().user_to_user_details_dto(u),
                        "account": AccountMapper.get_instance().account_to_account_details_dto(u.account)
                    }
                expiration_time = 604800  # 604800s = 7 days.
                now = int(time.time())
                payload = {
                    "username": u.username,
                    "email": u.email,
                    "iat": now,
                    "exp": now + expiration_time
                }
                u.token = jwt.encode(payload, secret_key, algorithm="HS256")
                session.commit()
                # return {"access_token": u.token, "user": u}
                return {
                    "access_token": u.token,
                    "user": UserMapper.get_instance().user_to_user_details_dto(u),
                    "account": AccountMapper.get_instance().account_to_account_details_dto(u.account)
                }
            except NoResultFound as e:
                # Password or username is incorrect or in fact username does not exist.
                logging.exception(f"DB Connection requested by user: '{username}' failed. Details: {e}")
                raise NotAuthorizedException()
            except Exception as e:  # Any other Exception
                logging.exception(f"DB Connection requested by user: '{username}' failed. Details: {e}")
                raise NotAuthorizedException()
        except Exception as e:
            raise e
        finally:
            if session:
                # session.expunge_all()
                session.close()
                logging.info(f"DB Connection requested by user: '{username}' closed.")

    def register_user(self, new_user: User) -> None:
        """
        Parameters:
            new_user: User made from client's input and validated by UserRegisterDTO.
        Returns:
            None: If new_user is registered correctly.
        """
        session = None
        try:
            if not new_user:
                raise MalformedRequestException("Invalid parameter 'new_user' exception")
            session = self.create_session()
            filters = ((User.username == new_user.username) | (User.email == new_user.email))
            try:
                u = session.query(User).filter(filters).one()  # Searching for a repeated instance.
                if u is not None:
                    if u.email == new_user.email:
                        raise ExistentRecordException("Existent 'email' exception")
                    if u.username == new_user.username:
                        raise ExistentRecordException("Existent 'username' exception")
            except NoResultFound as e:
                pass  # If entity was not found program shall continue normally.

            if not re.fullmatch(default_password_pattern(), new_user.password):
                raise MalformedRequestException("Invalid value for parameter 'password'")
            # Field name change and SHA256 hashing
            new_user.pwd_hash = hashlib.sha256(new_user.password.encode('utf-8')).hexdigest()
            new_user.creation_datetime = datetime.datetime.now()
            new_user.username = new_user.username.lower()
            new_user.email = new_user.email.lower()
            new_user.enabled = True
            new_user.first_name = new_user.first_name.title()
            new_user.last_name = new_user.last_name.title()
            # SO Role/Permission section
            default_role = RoleDAO.get_instance().export_default_client_role()
            session.object_session(default_role)
            session.add(default_role)
            new_user.roles = [default_role]
            default_role.users.append(new_user)
            # EO Role/Permission section
            # SO Account section
            account = Account(
                creation_datetime=datetime.datetime.now(),
                total_balance=0.0,
                owner_id=new_user.id,
                owner=new_user
            )
            session.object_session(account)
            session.add(account)
            # EO Account section
            session.add(new_user)
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

    def check_authorization_by_username(self, username, token) -> dict:
        """
        Parameters:
            username: username from a User that needs auth verification.
            token: Token to check if it is expired or not.
        Returns:
            dict:
        """
        session = None
        try:
            if not username:
                raise MalformedRequestException("Invalid parameter 'username' exception")
            if not token:
                raise MalformedRequestException("Invalid parameter 'token' exception")
            try:
                session = self.create_session()
                u = session.query(User).filter((User.username == username)).one()  # Searching for an
                # existent instance.
                if u.token and u.token == token:  # If token is not expired.
                    return {"user": UserMapper.get_instance().user_to_user_details_dto(u),
                            "account": AccountMapper.get_instance().account_to_account_details_dto(u.account)
                            }  # If the user is found successfully AND both tokens are equal.
                raise NotAuthorizedException("Not authorized")
            except NoResultFound as e:
                logging.exception(f"DB Connection failed. Details: {e}")
                raise NotAuthorizedException("Not authorized")
            except BaseException as e:  # Any other Exception
                logging.exception(f"DB Connection failed. Details: {e}")
                raise e

        except BaseException as e:  # Any other Exception
            logging.exception(f"DB Connection failed. Details: {e}")
            raise e
        finally:
            if session:
                # session.expunge_all()
                session.close()

    def check_authorization_by_token(self, token: str) -> bool:
        """
        Parameters:
            token: Token to check if it is valid or not.
        Returns:
            dict:
        """
        session = None
        try:
            if not token:
                raise MalformedRequestException("Invalid parameter 'token' exception")
            try:
                session = self.create_session()
                u = session.query(User).filter((User.token == token)).one()  # Searching for an
                # existent instance.
                if u.token:
                    return True
                raise NotAuthorizedException("Not authorized")
            except NoResultFound as e:
                logging.exception(f"DB Connection failed. Details: {e}")
                raise NotAuthorizedException("Not authorized")
            except BaseException as e:  # Any other Exception
                logging.exception(f"DB Connection failed. Details: {e}")
                raise e

        except BaseException as e:  # Any other Exception
            logging.exception(f"DB Connection failed. Details: {e}")
            raise e
        finally:
            if session:
                # session.expunge_all()
                session.close()

    def search_user_by_email(self, email: str):
        """
        Parameters:
            param email: email to search user.
        Returns:
            User: Existing user.
        """
        session = None
        try:
            session = self.create_session()
            user_result = session.query(User).filter((User.email == email)).one()
            if not user_result:
                raise NonExistentRecordException()
            return user_result
        except NoResultFound as e:
            logging.exception(f"DB Connection failed. Details: {e}")
            raise NonExistentRecordException
        finally:
            if session:
                session.close()

    def search_user_by_username(self, username: str):
        """
        Parameters:
            param username: username to search user.
        Returns:
            User: Existing user.
        """
        session = None
        try:
            session = self.create_session()
            filters = (User.username == username)
            user_result = session.query(User).filter(filters).one()
            if not user_result:
                raise NonExistentRecordException()
            return user_result
        except Exception as e:
            logging.exception(f"DB Connection failed. Details: {e}")
            raise e
        finally:
            if session:
                session.close()
