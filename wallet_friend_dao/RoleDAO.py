"""
@author: "Arnoldo J. González Quesada".
Github username: "ArnoldG6".
Contact me via "arnoldgq612@gmail.com".
GPL-3.0 license ©2022
"""
from __future__ import annotations
from enum import Enum

from wallet_friend_dao import DAO
from wallet_friend_exceptions.WalletFriendExceptions import SingletonObjectException


class ClientRole(Enum):
    """
    Class to define default-role info for client
    It is associated with all client permissions
    """
    NAME = "Client"
    DESCRIPTION = "Can access to common-user functions in the website"


class RoleDAO(DAO):
    """
    RoleDAO class  manages DB queries in order to use CRUD methods.
    """
    __role_dao_singleton = None  # Singleton RoleDAO object
    
    @staticmethod
    def get_instance() -> RoleDAO:
        """
        Returns:
            RoleDAO: the RoleDAO class singleton object.
        """
        if not RoleDAO.__role_dao_singleton:
            RoleDAO.__role_dao_singleton = RoleDAO()
        return RoleDAO.__role_dao_singleton

    def __init__(self):
        super().__init__()
        if RoleDAO.__role_dao_singleton:
            raise SingletonObjectException()
        else:
            RoleDAO.__role_dao_singleton = self
