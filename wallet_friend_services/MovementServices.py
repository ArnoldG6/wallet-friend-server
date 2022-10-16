"""
@author: "Arnoldo J. González Quesada".
Github username: "ArnoldG6".
Contact me via "arnoldgq612@gmail.com".
GPL-3.0 license ©2022
"""
import logging
from flask import request as f_request

from wallet_friend_dao.MovementDAO import MovementDAO
from wallet_friend_dto.MovementDTO import MovementAddDTO
from wallet_friend_exceptions.HttpWalletFriendExceptions import ExpiredRequestException, ExistentRecordException, \
    MalformedRequestException
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
                add_movement_dto = MovementAddDTO(**self.__request.get_json())
                new_movement = MovementMapper.get_instance().movement_add_dto_to_movement(add_movement_dto)
                MovementDAO.get_instance().add(new_movement, add_movement_dto.owner)
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
