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
    MalformedRequestException, NonExistentRecordException, HttpWalletFriendException
from wallet_friend_mappers.MovementMapper import MovementMapper
from wallet_friend_services import AuthService


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
            AuthService(self.__request).check_authorization_user_service_by_token()
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
            except BaseException as e:
                logging.exception(e)
                raise e
            except HttpWalletFriendException as e:
                logging.exception(e)
                raise e
        except HttpWalletFriendException as e:
            logging.exception(e)
            raise e
        except BaseException as e:
            logging.exception(e)
            raise e

    def delete_movement_service(self, movement_id: int):
        """
        Returns:
            None: if movement is registered correctly.
        """
        try:

            if not self.__request:
                raise ExpiredRequestException()
            AuthService(self.__request).check_authorization_user_service_by_token()
            try:
                if movement_id is None:
                    raise MalformedRequestException("Invalid parameter 'movement_id'.")
                MovementDAO.get_instance().delete(movement_id)
            except ValueError as e:
                logging.exception(e)
                raise MalformedRequestException
            except NonExistentRecordException as e:
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

    def add_bag_movement_to_movement_service(self):
        """
          Returns:
              None: if BagMovement is registered correctly.
          """
        try:
            AuthService(self.__request).check_authorization_user_service_by_token()
            try:
                movement_id = self.__request.get_json().get("movement_id", None)
                if not movement_id:
                    raise MalformedRequestException("Missing field 'movement_id'.")
                bag_id = self.__request.get_json().get("bag_id", None)
                if not bag_id:
                    raise MalformedRequestException("Missing field 'bag_id'.")
                amount = self.__request.get_json().get("amount", None)
                if not amount:
                    raise MalformedRequestException("Missing field 'amount'.")

                MovementDAO.get_instance().add_bag_movement_to_movement(
                    movement_id, bag_id, amount
                )
            except ValueError as e:
                logging.exception(e)
                raise MalformedRequestException
            except NonExistentRecordException as e:
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
