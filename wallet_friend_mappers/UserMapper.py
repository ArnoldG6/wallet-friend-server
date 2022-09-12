"""
@author: "Arnoldo J. González Quesada".
Github username: "ArnoldG6".
Contact me via "arnoldgq612@gmail.com".
GPL-3.0 license ©2022
"""
from __future__ import annotations

from wallet_friend_dto import UserDetailsDTO
from wallet_friend_entities import User
from wallet_friend_exceptions.WalletFriendExceptions import SingletonObjectException
from wallet_friend_mappers.RoleMapper import RoleMapper


class UserMapper:
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
        user_d = u.__dict__
        user_d["roles"] = RoleMapper.get_instance().role_list_to_role_details_dto_list(u.roles)
        return UserDetailsDTO(**user_d)

    """
    ==========================Input-purpose-mapping.==========================
    """

    def user_register_dto_to_user(self, user_register_dto):
        u = User()
        for k, v in user_register_dto.dict().items():
            u.__dict__[k] = v
        return u
