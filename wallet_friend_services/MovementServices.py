"""
@author: "Arnoldo J. González Quesada".
Github username: "ArnoldG6".
Contact me via "arnoldgq612@gmail.com".
GPL-3.0 license ©2022
"""
import logging
from flask import request as f_request

from wallet_friend_dao.FixedMovementDAO import FixedMovementDAO
from wallet_friend_dao.MovementDAO import MovementDAO
from wallet_friend_dto.FixedMovementDTO import FixedMovementAddDTO
from wallet_friend_dto.MovementDTO import MovementAddDTO
from wallet_friend_exceptions.HttpWalletFriendExceptions import ExpiredRequestException, ExistentRecordException, \
    MalformedRequestException
from wallet_friend_mappers.FixedMovementMapper import FixedMovementMapper
from wallet_friend_mappers.MovementMapper import MovementMapper


class MovementService:
    """
    The present class manages HTTP client requests that depends on
    Movement class objects information and operations.
    """

    def __init__(self, request: f_request):
        if request is None:
            raise ExpiredRequestException()
        self.__request = request

    def create_single_movement_service(self):
        """
        Returns:
            None: if movement is registered correctly.
        """
        try:
            if not self.__request:
                raise ExpiredRequestException()
            try:
                MovementDAO.get_instance().add(
                    MovementMapper.get_instance().
                    movement_add_dto_to_movement(
                        MovementAddDTO(**self.__request.get_json())
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
