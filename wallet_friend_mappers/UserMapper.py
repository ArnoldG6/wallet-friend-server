"""
@author: "Arnoldo J. González Quesada".
Github username: "ArnoldG6".
Contact me via "arnoldgq612@gmail.com".
GPL-3.0 license ©2022
"""
from __future__ import annotations

import logging

from wallet_friend_dto import UserDetailsDTO
from wallet_friend_entities import User
from wallet_friend_exceptions.HttpWalletFriendExceptions import MalformedRequestException
from wallet_friend_exceptions.WalletFriendExceptions import SingletonObjectException
from wallet_friend_mappers.AccountMapper import AccountMapper
from wallet_friend_mappers.Mapper import Mapper
from wallet_friend_mappers.RoleMapper import RoleMapper



class UserMapper(Mapper):
    """
    UserMapper translate UserDTO objects into User objects and vice-versa.
    """
    user_mapper_singleton = None  # Singleton UserMapper object

    @staticmethod
    def get_instance() -> UserMapper:
        """
        Returns:
            user_mapper_singleton: the UserMapper's class singleton object.
        """
        if UserMapper.user_mapper_singleton is None:
            UserMapper.user_mapper_singleton = UserMapper()
        return UserMapper.user_mapper_singleton

    def __init__(self):
        super().__init__()
        if UserMapper.user_mapper_singleton is not None:
            raise SingletonObjectException()
        else:
            UserMapper.user_mapper_singleton = self

    """
    ==========================Outer-purpose-mapping.==========================
    """

    def user_to_user_details_dto(self, u):
        try:
            user_d = u.__dict__
            user_d["roles"] = RoleMapper.get_instance().role_list_to_role_details_dto_list(u.roles)
            #user_d["account"] = AccountMapper.get_instance().
            return UserDetailsDTO(**user_d)
        except ValueError as e:
            logging.exception(e)
            raise MalformedRequestException(str(e))
        except MalformedRequestException as e:
            logging.exception(e)
            raise e
        except BaseException as e:
            logging.exception(e)
            raise MalformedRequestException()

    """
    ==========================Input-purpose-mapping.==========================
    """

    def user_register_dto_to_user(self, user_register_dto):
        try:
            u = User()
            u.__dict__ |= user_register_dto.dict()
            return u
        except ValueError as e:
            logging.exception(e)
            raise MalformedRequestException(str(e))
        except MalformedRequestException as e:
            logging.exception(e)
            raise e
        except BaseException as e:
            logging.exception(e)
            raise MalformedRequestException()
