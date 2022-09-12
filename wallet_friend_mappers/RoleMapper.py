"""
@author: "Arnoldo J. González Quesada".
Github username: "ArnoldG6".
Contact me via "arnoldgq612@gmail.com".
GPL-3.0 license ©2022
"""
from __future__ import annotations

import logging

from wallet_friend_dto.RoleDTO import RoleDetailsDTO
from wallet_friend_exceptions.HttpWalletFriendExceptions import MalformedRequestException
from wallet_friend_mappers.PermissionMapper import PermissionMapper


class RoleMapper:
    """
    RoleMapper translate RoleDTO objects into Role objects and vice-versa.
    """
    role_mapper_singleton = None  # Singleton RoleMapper object

    @staticmethod
    def get_instance() -> RoleMapper:
        """
        Returns:
            role_mapper_singleton: the RoleMapper's class singleton object.
        """
        if RoleMapper.role_mapper_singleton is None:
            RoleMapper.role_mapper_singleton = RoleMapper()
        return RoleMapper.role_mapper_singleton

    def __init__(self):
        super().__init__()
        if RoleMapper.role_mapper_singleton is not None:
            raise Exception("Singleton Class Exception")
        else:
            RoleMapper.role_mapper_singleton = self

    """
    ==========================Outer-purpose-mapping.==========================
    """

    def role_to_role_details_dto(self, role):
        """
        Params:
            role: Role object to be translated.
        Returns:
            RoleDetailsDTO object.
        """
        try:
            role_d = role.dict_rep()
            role_d["permissions"] = PermissionMapper.get_instance(). \
                permission_list_to_permission_details_dto_list(role_d["permissions"])
            return RoleDetailsDTO(**role_d)
        except MalformedRequestException as e:
            logging.error(e)
            raise e

    def role_list_to_role_details_dto_list(self, role_list):
        """
        Params:
            role_list: List of Role objects to be translated.
        Returns:
            A list of RoleDetailsDTO objects.
        """
        try:
            return [self.role_to_role_details_dto(r) for r in role_list]
        except MalformedRequestException as e:
            logging.error(e)
            raise e
