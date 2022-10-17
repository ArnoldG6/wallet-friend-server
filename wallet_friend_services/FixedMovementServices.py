"""
@author: "Arnoldo J. González Quesada".
Github username: "ArnoldG6".
Contact me via "arnoldgq612@gmail.com".
GPL-3.0 license ©2022
"""
import logging

from flask import request as f_request

from wallet_friend_dao.FixedMovementDAO import FixedMovementDAO
from wallet_friend_dto.FixedMovementDTO import FixedMovementAddDTO
from wallet_friend_exceptions.HttpWalletFriendExceptions import ExpiredRequestException, ExistentRecordException, \
    MalformedRequestException
from wallet_friend_mappers.FixedMovementMapper import FixedMovementMapper


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

            try:
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
            except Exception as e:
                logging.exception(e)
                raise e


        except Exception as e:
            logging.exception(e)
            raise e
