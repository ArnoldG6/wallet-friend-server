"""
@author: "Arnoldo J. González Quesada".
Github username: "ArnoldG6".
Contact me via "arnoldgq612@gmail.com".
GPL-3.0 license ©2022
"""
import logging

from flask import request as f_request

from wallet_friend_dao import UserDAO
from wallet_friend_dto import UserAuthDTO, UserDetailsDTO
from wallet_friend_tools import check_non_empty_non_spaces_string


class AuthService:
    """
    The present class manages HTTP client requests that depends on
    User class objects information and operations.
    """

    def __init__(self, request: f_request):
        if request is None:
            raise Exception("Expired request exception")
        self.__request = request

    def auth_user_service(self, secret_key: str) -> dict:  # []
        """
        Parameters:
             secret_key: key used to generate JWT.
        Returns:
            dict: an authorized User object.
                {
                    "user:" UserDetailsDTO,
                    "access_token": access_token
                }
        """
        if not check_non_empty_non_spaces_string(secret_key):
            raise Exception("Invalid parameter 'secret_key' exception")
        try:
            if self.__request is not None:
                a = UserAuthDTO(**self.__request.get_json())
                result = UserDAO.get_instance().auth_user(a, secret_key)
                result["user"] = UserDetailsDTO(**result["user"].dict_rep())  # Converts User to UserDetailsDTO
                return result
            else:
                raise Exception("Expired request exception")
        except Exception as e:
            logging.error(e)
            raise e
