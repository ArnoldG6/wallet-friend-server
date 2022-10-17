"""
@author: "Arnoldo J. González Quesada".
Github username: "ArnoldG6".
Contact me via "arnoldgq612@gmail.com".
GPL-3.0 license ©2022
"""
from __future__ import annotations

import datetime
import logging
from enum import Enum

from sqlalchemy.orm.exc import NoResultFound

from wallet_friend_dao.PermissionDAO import ClientPermission
from wallet_friend_entities import Role, Permission
from wallet_friend_exceptions.WalletFriendExceptions import SingletonObjectException
from wallet_friend_settings import default_db_settings_path
from .DAO import DAO


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
    def get_instance(path=default_db_settings_path()) -> RoleDAO:
        """
        Returns:
            RoleDAO: the RoleDAO class singleton object.
        """
        if not RoleDAO.__role_dao_singleton:
            RoleDAO.__role_dao_singleton = RoleDAO(path)
        return RoleDAO.__role_dao_singleton

    def __init__(self, path=default_db_settings_path()):
        super().__init__(path)
        if RoleDAO.__role_dao_singleton:
            raise SingletonObjectException()
        else:
            RoleDAO.__role_dao_singleton = self

    def export_default_client_role(self) -> Role:
        """
        Returns:
            Role: default client role
        """
        role_session = None
        try:
            role_session = self.create_session()
            role_session.expire_on_commit = False
            try:
                r = role_session.query(Role).filter((Role.name == ClientRole.NAME.value)).one()  # Searching for a
                # repeated instance.
                if r is not None:
                    return r
            except NoResultFound as e:
                pass  # If entity was not found program shall continue normally.

            client_permission = Permission()
            client_permission.__dict__ |= {
                "creation_datetime": datetime.datetime.now(),
                "name": ClientPermission.NAME.value,
                "description": ClientPermission.DESCRIPTION.value
            }
            client_role = Role()
            client_role.__dict__ |= {
                "creation_datetime": datetime.datetime.now(),
                "name": ClientRole.NAME.value,
                "description": ClientRole.DESCRIPTION.value
            }

            role_session.add(client_permission)
            role_session.add(client_role)
            client_role.permissions = [client_permission]
            client_permission.roles = [client_role]
            role_session.commit()
            return client_role
        except Exception as e:  # Any other Exception
            logging.exception(f"DB Connection failed. Details: {e}")
            raise e
        finally:
            if role_session:
                role_session.close()
