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
    ExistentRecordException, NotAuthorizedException
from wallet_friend_exceptions.WalletFriendExceptions import IncorrectParameterValueException
from wallet_friend_manager import CodeManager, EmailManager
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
                    logging.exception(e)
                    raise MalformedRequestException()
                except ValueError as e:
                    logging.exception(e)
                    raise MalformedRequestException()
            else:
                raise ExpiredRequestException()
        except Exception as e:
            logging.exception(e)
            raise e

    def register_user_service(self):
        """
        Returns:
            None: if user is registered correctly.
        """
        try:
            if self.__request is not None:
                try:
                    new_user = UserMapper.get_instance(). \
                        user_register_dto_to_user(UserRegisterDTO(**self.__request.get_json()))
                    UserDAO.get_instance().register_user(new_user)
                except ValueError as e:
                    logging.exception(e)
                    raise MalformedRequestException()
                except ExistentRecordException as e:
                    logging.exception(e)
                    raise e
                except Exception as e:
                    logging.exception(e)
                    raise e
            else:
                raise ExpiredRequestException()
        except Exception as e:
            logging.exception(e)
            raise e

    def check_authorization_user_service(self, username: str) -> dict:  # []
        """
        Parameters:
            username: Username that the client is asking for his authorization state.
        """
        try:
            if not username:
                raise MalformedRequestException("Invalid path parameter 'username' exception")
            if self.__request is not None:
                try:
                    if self.__request.headers["Authorization"] is None:
                        raise MalformedRequestException("Invalid path parameter 'token'")
                    auth_token = self.__request.headers["Authorization"].split()
                    # Auth token comes in format: "Bearer xxxxx....."
                    if len(auth_token) != 2 or not auth_token[-1] or auth_token[-1] == "null":
                        raise MalformedRequestException("Invalid path parameter 'token'")
                    # No UserDTO-mapping is required.

                    user = UserDAO.get_instance().check_authorization_by_username(username, auth_token[-1])
                    return {"user": UserMapper.get_instance().user_to_user_details_dto(user)}
                except NotAuthorizedException as e:
                    logging.exception(e)
                    raise e
                except MalformedRequestException as e:
                    logging.exception(e)
                    raise e
                except BaseException as e:
                    logging.exception(e)
                    raise e
            else:
                raise ExpiredRequestException()
        except BaseException as e:
            logging.exception(e)
            raise e

    def reset_password_service(self, latestVersion : int):
        try:
            if self.__request is not None:
                self.__request.ge
                email = 'sample@email.com' # Retrieve user email from session is missing to do
                user = UserDAO.get_instance().search_user_by_email(email)
                number_reset = CodeManager.get_instance().add_code(user)
                link_reset = f"/api/{latestVersion}/users/reset_password/{number_reset}"
                EmailManager.get_instance().send_reset_password(user, link_reset)
            #Adding more specific ex is missing to do
        except Exception as e:
            logging.error(e)
            raise e

    def change_password_service(self):
        try:
            pass

        except Exception as e:
            logging.error(e)
            raise e