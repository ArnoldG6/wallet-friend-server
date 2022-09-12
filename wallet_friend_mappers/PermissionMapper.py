"""
@author: "Arnoldo J. González Quesada".
Github username: "ArnoldG6".
Contact me via "arnoldgq612@gmail.com".
GPL-3.0 license ©2022
"""
from __future__ import annotations

import logging
from typing import List

from pydantic import parse_obj_as
from wallet_friend_dto import UserDetailsDTO
from wallet_friend_dto.PermissionDTO import PermissionDetailsDTO
from wallet_friend_entities import User, Permission, Role
from wallet_friend_exceptions.HttpWalletFriendExceptions import MalformedRequestException


class PermissionMapper:
    """
    PermissionMapper translate PermissionDTO objects into User objects and vice-versa.
    """
    permission_mapper_singleton = None  # Singleton PermissionMapper object

    @staticmethod
    def get_instance() -> PermissionMapper:
        """
        Returns:
            permission_mapper_singleton: the PermissionMapper's class singleton object.
        """
        if PermissionMapper.permission_mapper_singleton is None:
            PermissionMapper.permission_mapper_singleton = PermissionMapper()
        return PermissionMapper.permission_mapper_singleton

    def __init__(self):
        super().__init__()
        if PermissionMapper.permission_mapper_singleton is not None:
            raise Exception("Singleton Class Exception")
        else:
            PermissionMapper.permission_mapper_singleton = self
    """
    ==========================Outer-purpose-mapping.==========================
    """

    def permission_to_permission_details_dto(self, permission):
        """
        Params:
            permission: Permission object to be translated.
        Returns:
            PermissionDetailsDTO object.
        """
        try:
            return PermissionDetailsDTO(**permission.__dict__)
        except MalformedRequestException as e:
            logging.error(e)
            raise e

    def permission_list_to_permission_details_dto_list(self, permission_list):
        """
        Params:
            permission_list: List of Permission objects to be translated.
        Returns:
            A list of PermissionDetailsDTO objects.
        """
        try:
            return parse_obj_as(List[PermissionDetailsDTO], [p.__dict__ for p in permission_list])

        except MalformedRequestException as e:
            logging.error(e)
            raise e
