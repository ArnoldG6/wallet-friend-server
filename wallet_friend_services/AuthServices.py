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
from wallet_friend_dto.UserDTO import UserRegisterDTO
from wallet_friend_exceptions.HttpWalletFriendExceptions import MalformedRequestException, ExpiredRequestException, \
    InternalServerException
from wallet_friend_exceptions.WalletFriendExceptions import IncorrectParameterValueException
from wallet_friend_mappers.UserMapper import UserMapper
from wallet_friend_tools import check_non_empty_non_spaces_string


class AuthService:
    """
    The present class manages HTTP client requests that depends on
    User class objects information and operations.
    """

    def __init__(self, request: f_request):
        if request is None:
            raise ExpiredRequestException()
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
        try:
            if not check_non_empty_non_spaces_string(secret_key):
                raise IncorrectParameterValueException("Invalid parameter 'secret_key' exception")
            if self.__request is not None:
                try:
                    result = UserDAO.get_instance().auth_user(UserAuthDTO(**self.__request.get_json()), secret_key)
                    result["user"] = UserMapper.get_instance(). \
                        user_to_user_details_dto(result["user"])  # Converts User to UserDetailsDTO
                    return result
                except pydantic.error_wrappers.ValidationError as e:
                    logging.error(e)
                    raise MalformedRequestException()
                except ValueError as e:
                    logging.error(e)
                    raise MalformedRequestException()
            else:
                raise ExpiredRequestException()
        except Exception as e:
            logging.error(e)
            raise InternalServerException()

    def register_user_service(self):
        """
        Returns:
            UserDetailsDTO object of the new registered user.
        """
        try:
            if self.__request is not None:
                try:
                    new_user = UserMapper.get_instance(). \
                        user_register_dto_to_user(UserRegisterDTO(**self.__request.get_json()))
                    return {
                        "user": UserMapper.get_instance().
                        user_to_user_details_dto(UserDAO.get_instance().register_user(new_user))
                    }
                except ValueError as e:
                    logging.error(e)
                    raise MalformedRequestException()
                except Exception as e:
                    logging.error(e)
                    raise e
            else:
                raise ExpiredRequestException()
        except Exception as e:
            logging.error(e)
            raise e
