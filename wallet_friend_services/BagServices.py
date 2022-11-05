"""
@author: "Arnoldo J. González Quesada".
Github username: "ArnoldG6".
Contact me via "arnoldgq612@gmail.com".
GPL-3.0 license ©2022
"""
import logging
from flask import request as f_request
from datetime import datetime
from wallet_friend_dao.BagDAO import BagDAO
from wallet_friend_dto.BagDTO import BagAddDTO
from wallet_friend_exceptions.HttpWalletFriendExceptions import ExpiredRequestException, MalformedRequestException, \
    ExistentRecordException, HttpWalletFriendException, NonExistentRecordException
from wallet_friend_mappers.BagMapper import BagMapper
from wallet_friend_services import AuthService


class BagService:
    """
    The present class manages HTTP client requests that depends on
    Bag class objects information and operations.
    """

    def __init__(self, request: f_request):
        if request is None:
            raise ExpiredRequestException()
        self.__request = request

    def add_bag(self):
        """
          Returns:
              None: if Bag is registered correctly.
          """
        try:
            AuthService(self.__request).check_authorization_user_service_by_token()
            try:
                if not self.__request.get_json().get("end_date", None):
                    raise MalformedRequestException("Missing field 'end_date'")
                self.__request.get_json()["end_date"] = \
                    datetime.strptime(self.__request.get_json()["end_date"], '%d/%m/%Y')
                BagDAO.get_instance().add(
                    BagMapper.get_instance().bag_add_dto_to_bag(
                        BagAddDTO(**self.__request.get_json())
                    )
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

    def delete_bag(self, bag_id: int):
        """
          Returns:
              None: if Bag is deleted correctly.
          """
        try:
            if bag_id is None:
                raise MalformedRequestException("Missing field 'bag_id'")
            BagDAO.get_instance().delete(bag_id)
        except HttpWalletFriendException as e:
            logging.exception(e)
            raise e
        except BaseException as e:
            logging.exception(e)
            raise e