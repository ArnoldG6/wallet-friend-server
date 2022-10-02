"""
@author: "Arnoldo J. González Quesada".
Github username: "ArnoldG6".
Contact me via "arnoldgq612@gmail.com".
GPL-3.0 license ©2022
"""
from __future__ import annotations

import logging
import datetime
from enum import Enum
from sqlalchemy.orm.exc import NoResultFound
from .DAO import DAO
from wallet_friend_dao.PermissionDAO import ClientPermission
from wallet_friend_entities import Role, Permission
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
    def get_instance(path="wallet_friend_db/config.ini") -> RoleDAO:
        """
        Returns:
            RoleDAO: the RoleDAO class singleton object.
        """
        if not RoleDAO.__role_dao_singleton:
            RoleDAO.__role_dao_singleton = RoleDAO(path)
        return RoleDAO.__role_dao_singleton

    def __init__(self, path="wallet_friend_db/config.ini"):
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
        session = None
        try:
            session = self.create_session()
            try:
                r = session.query(Role).filter((Role.name == ClientRole.NAME.value)).one()  # Searching for a
                # repeated instance.
                if r is not None:
                    return r
            except NoResultFound as e:
                pass  # If entity was not found program shall continue normally.

            client_permission = Permission(creation_datetime=datetime.datetime, name=ClientPermission.NAME.value,
                                           description=ClientPermission.DESCRIPTION.value)
            role = Role(name=ClientRole.NAME.value, description=ClientRole.DESCRIPTION.value,
                        creation_datetime=datetime.datetime, permissions=[client_permission])
            client_permission.roles = [role]
            session.add(role)
            session.commit()
            return role
        except Exception as e:  # Any other Exception
            logging.exception(f"DB Connection failed. Details: {e}")
            raise e
        finally:
            if session:
                session.close()
