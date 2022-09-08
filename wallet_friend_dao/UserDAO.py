"""
@author: "Arnoldo J. González Quesada".
Github username: "ArnoldG6".
Contact me via "arnoldgq612@gmail.com".
GPL-3.0 license ©2022
"""
from __future__ import annotations
import logging
import time
import jwt

from .GenericDAO import GenericDAO
from wallet_friend_dto import UserAuthDTO
from wallet_friend_entities import User
from wallet_friend_tools import check_non_empty_non_spaces_string


class UserDAO(GenericDAO):
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
            raise Exception("Singleton Class Exception")
        else:
            UserDAO.__user_dao_singleton = self

    def auth_user(self, user_auth_dto: UserAuthDTO, secret_key: str) -> dict or None:
        """
        Parameters:
            secret_key(str):
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
                raise Exception("Invalid parameter 'pwd' exception")
            if not check_non_empty_non_spaces_string(username):
                raise Exception("Invalid parameter 'username' exception")
            if not check_non_empty_non_spaces_string(secret_key):
                raise Exception("Invalid parameter 'secret_key' exception")
            session = self.get_session()
            logging.info(f"DB Connection requested by user: '{username}' is established.")
            try:
                filters = (((User.username == username) | (User.email == username)) & (User.pwd_hash == pwd))
                u = self.get_session().query(User).filter(filters).one()
                expiration_time = 604800  # 604800s = 7 days.
                now = int(time.time())
                payload = {
                    "username": u.username,
                    "email": u.email,
                    "iat": now,
                    "exp": now + expiration_time
                }
                access_token = jwt.encode(payload, secret_key, algorithm="HS256")
                return {"access_token": access_token, "user": u}
            except Exception as e:
                logging.exception(f"DB Connection requested by user: '{username}' failed. Details: {e}")
                raise Exception("Not authorized")
        except Exception as e:
            raise e
        finally:
            if session:
                logging.info(f"DB Connection requested by user: '{username}' closed.")

