"""
@author: "Arnoldo J. González Quesada".
Github username: "ArnoldG6".
Contact me via "arnoldgq612@gmail.com".
GPL-3.0 license ©2022
"""
from __future__ import annotations

import datetime
import logging
import re
import time
import hashlib

import jwt
from sqlalchemy.orm.exc import NoResultFound

from wallet_friend_dto import UserAuthDTO
from wallet_friend_entities import User
from wallet_friend_exceptions.HttpWalletFriendExceptions import NotAuthorizedException, DisabledUserException, \
    MalformedRequestException, ExistentEntityException
from wallet_friend_exceptions.WalletFriendExceptions import SingletonObjectException
from wallet_friend_settings import default_password_pattern
from wallet_friend_tools import check_non_empty_non_spaces_string
from .DAO import DAO


class UserDAO(DAO):
    """
    DBHandler class  manages the mqd_db queries in order to use CRUD methods.
    """
    __user_dao_singleton = None  # Singleton UserDAO object

    @staticmethod
    def get_instance() -> UserDAO:
        """
        Returns:
            UserDAO: the UserDAO class singleton object.
        """
        if UserDAO.__user_dao_singleton is None:
            UserDAO.__user_dao_singleton = UserDAO()
        return UserDAO.__user_dao_singleton

    def __init__(self):
        super().__init__()
        if UserDAO.__user_dao_singleton is not None:
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
            session = self.get_session()
            logging.info(f"DB Connection requested by user: '{username}' is established.")
            try:
                filters = (((User.username == username) | (User.email == username)) & (User.pwd_hash == pwd))
                u = self.get_session().query(User).filter(filters).one()
                if not u:
                    raise NotAuthorizedException()
                if not u.enabled:  # If user is disabled.
                    raise DisabledUserException()
                if u.token:
                    return {"access_token": u.token, "user": u}
                expiration_time = 604800  # 604800s = 7 days.
                now = int(time.time())
                payload = {
                    "username": u.username,
                    "email": u.email,
                    "iat": now,
                    "exp": now + expiration_time
                }
                u.token = jwt.encode(payload, secret_key, algorithm="HS256")
                self.get_session().commit()
                return {"access_token": u.token, "user": u}
            except NoResultFound as e:
                # Password or username is incorrect or in fact username does not exist.
                logging.error(f"DB Connection requested by user: '{username}' failed. Details: {e}")
                raise NotAuthorizedException()
            except Exception as e:  # Any other Exception
                logging.error(f"DB Connection requested by user: '{username}' failed. Details: {e}")
                raise NotAuthorizedException()
        except Exception as e:
            raise e
        finally:
            if session:
                logging.info(f"DB Connection requested by user: '{username}' closed.")

    def register_user(self, new_user: User) -> User:
        """
        Parameters:
            param new_user: User made from client's input and validated by UserRegisterDTO.
        Returns:
            User: Freshly-created and registered user.
        """
        session = None
        try:
            if not new_user:
                raise MalformedRequestException("Invalid parameter 'new_user' exception")
            username = new_user.username
            email = new_user.email
            session = self.get_session()
            filters = ((User.username == username) | (User.email == email))
            try:
                u = self.get_session().query(User).filter(filters).one()  # Searching for a repeated instance.
                if u is not None:
                    if u.email == new_user.email:
                        raise ExistentEntityException("Existent 'email' exception")
                    if u.username == new_user.username:
                        raise ExistentEntityException("Existent 'username' exception")
            except NoResultFound as e:
                pass  # If entity was not found program shall continue normally.

            if not re.fullmatch(default_password_pattern(), new_user.password):
                raise MalformedRequestException("Invalid value for parameter 'password'")
            # Field name change and SHA256 hashing
            new_user.pwd_hash = hashlib.sha256(new_user.password.encode('utf-8')).hexdigest()
            new_user.creation_datetime = datetime.datetime.now()
            new_user.enabled = True
            new_user.roles = []
            self.get_session().add(new_user)
            self.get_session().commit()
            return new_user
        except ExistentEntityException as e:
            logging.error(e)
            raise e
        except Exception as e:  # Any other Exception
            logging.error(f"DB Connection failed. Details: {e}")
            raise e

    def search_user_by_email(self, email: str):
        """
        Parameters:
            param email: email to search user.
        Returns:
            User: Exisitng user.
        """
        try:
            filters = (User.email == email)
            user_result = self.get_session().query(User).filter(filters).one()
            if not user_result:
                raise NotAuthorizedException()
            return user_result
        except Exception as e:
            logging.error(f"DB Connection failed. Details: {e}")
            raise e