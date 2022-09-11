"""
@author: "Arnoldo J. González Quesada".
Github username: "ArnoldG6".
Contact me via "arnoldgq612@gmail.com".
GPL-3.0 license ©2022
"""
import logging

import pydantic
from flask import request as f_request

from wallet_friend_dao import UserDAO
from wallet_friend_dto import UserAuthDTO
from wallet_friend_exceptions.WalletFriendExceptions import MalformedRequestException
from wallet_friend_mappers.UserMapper import UserMapper
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
                try:
                    result = UserDAO.get_instance().auth_user(UserAuthDTO(**self.__request.get_json()), secret_key)
                    result["user"] = UserMapper.get_instance(). \
                        user_to_user_details_dto(result["user"])  # Converts User to UserDetailsDTO
                    return result
                except pydantic.error_wrappers.ValidationError:
                    raise MalformedRequestException()
            else:
                raise Exception("Expired request exception")
        except Exception as e:
            logging.error(e)
            raise e
