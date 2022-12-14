"""
@author: "Arnoldo J. González Quesada".
Github username: "ArnoldG6".
Contact me via "arnoldgq612@gmail.com".
GPL-3.0 license ©2022
"""
import logging
from datetime import datetime

from flask import request as f_request

from wallet_friend_dao.FixedMovementDAO import FixedMovementDAO
from wallet_friend_dto.FixedMovementDTO import FixedMovementAddDTO
from wallet_friend_exceptions.HttpWalletFriendExceptions import ExpiredRequestException, ExistentRecordException, \
    MalformedRequestException, HttpWalletFriendException
from wallet_friend_mappers.FixedMovementMapper import FixedMovementMapper
from wallet_friend_services import AuthService


class FixedMovementService:
    """
    The present class manages HTTP client requests that depends on
    Movement class objects information and operations.
    """

    def __init__(self, request: f_request):
        if request is None:
            raise ExpiredRequestException()
        self.__request = request

    def create_fixed_movement_service(self):
        try:
            if not self.__request:
                raise ExpiredRequestException()
            AuthService(self.__request).check_authorization_user_service_by_token()
            try:
                if not self.__request.get_json().get("repeat_date", None):
                    raise MalformedRequestException("Missing field 'repeat_date'")
                self.__request.get_json()["repeat_date"] = \
                    datetime.strptime(self.__request.get_json()["repeat_date"], '%d/%m/%Y')
                FixedMovementDAO.get_instance().add(
                    FixedMovementMapper.get_instance().
                    fixed_movement_add_dto_to_fixed_movement(
                        FixedMovementAddDTO(**self.__request.get_json())
                    )
                )

            except ValueError as e:
                logging.exception(e)
                raise MalformedRequestException
            except ExistentRecordException as e:
                logging.exception(e)
                raise e
            except BaseException as e:
                logging.exception(e)
                raise e

        except HttpWalletFriendException as e:
            logging.exception(e)
            raise e
        except BaseException as e:
            logging.exception(e)
            raise e
