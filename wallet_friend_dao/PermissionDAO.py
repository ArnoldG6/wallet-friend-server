"""
@author: "Arnoldo J. González Quesada".
Github username: "ArnoldG6".
Contact me via "arnoldgq612@gmail.com".
GPL-3.0 license ©2022
"""
from __future__ import annotations

from enum import Enum

from wallet_friend_exceptions.WalletFriendExceptions import SingletonObjectException
from wallet_friend_settings import default_db_settings_path
from .DAO import DAO


class ClientPermission(Enum):
    """
    Class to define default-permission info for client
    It is associated with all client-related permissions.
    """
    NAME = "Set account balance"
    DESCRIPTION = "User can add or withdraw money-representation from account"


class PermissionDAO(DAO):
    """
    PermissionDAO class  manages DB queries in order to use CRUD methods.
    """
    __permission_dao_singleton = None  # Singleton PermissionDAO object

    @staticmethod
    def get_instance(path=default_db_settings_path()) -> PermissionDAO:
        """
        Returns:
            PermissionDAO: the PermissionDAO class singleton object.
        """
        if not PermissionDAO.__permission_dao_singleton:
            PermissionDAO.__permission_dao_singleton = PermissionDAO(path)
        return PermissionDAO.__permission_dao_singleton

    def __init__(self, path=default_db_settings_path()):
        super().__init__(path)
        if PermissionDAO.__permission_dao_singleton:
            raise SingletonObjectException()
        else:
            PermissionDAO.__permission_dao_singleton = self
