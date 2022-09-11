"""
@author: "Arnoldo J. González Quesada".
Github username: "ArnoldG6".
Contact me via "arnoldgq612@gmail.com".
GPL-3.0 license ©2022
"""
from __future__ import annotations

from typing import List

from pydantic import parse_obj_as
from wallet_friend_dto import UserDetailsDTO
from wallet_friend_entities import User, Permission, Role
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
            raise Exception("Singleton Class Exception")
        else:
            UserMapper.user_mapper_singleton = self

    def user_to_user_details_dto(self, u):
        user_d = u.__dict__
        user_d["roles"] = RoleMapper.get_instance().role_list_to_role_details_dto_list(u.roles)
        return UserDetailsDTO(**user_d)



