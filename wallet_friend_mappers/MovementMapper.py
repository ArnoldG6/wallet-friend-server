"""
@author: "Miguel González Carvajal".
Github username: "Miguelgonz98".
Contact me via "mgonzalex236@gmail.com".
GPL-3.0 license ©2022
"""
from sqlalchemy.testing.plugin.plugin_base import logging

from wallet_friend_dto.MovementDTO import MovementDetailsDTO
from wallet_friend_entities.Entities import Movement
from wallet_friend_exceptions.HttpWalletFriendExceptions import MalformedRequestException
from wallet_friend_exceptions.WalletFriendExceptions import SingletonObjectException
from wallet_friend_mappers.Mapper import Mapper


class MovementMapper(Mapper):
    """
    MovementMapper translate MovementDTO objects into Movement objects and vice-versa.
    """
    movement_mapper_singleton = None  # Singleton MovementMapper object

    @staticmethod
    def get_instance():
        """
        Returns:
            movement_mapper_singleton: the MovementMapper's class singleton object.
        """
        if MovementMapper.movement_mapper_singleton is None:
            MovementMapper.movement_mapper_singleton = MovementMapper()
        return MovementMapper.movement_mapper_singleton

    def __init__(self):
        super().__init__()
        if MovementMapper.movement_mapper_singleton is not None:
            raise SingletonObjectException()
        else:
            MovementMapper.movement_mapper_singleton = self

    """
    ==========================Outer-purpose-mapping.==========================
    """

    def movement_to_movement_details_dto(self, u):
        try:
            movement_d = u.__dict__
            movement_d["bagMovements"] = BagMovementMapper.get_instance(). \
                bag_movement_list_to_bag_movement_details_dto_list(u.bagMovements)
            return MovementDetailsDTO(**movement_d)

        except MalformedRequestException as e:
            logging.exception(e)
            raise e
        except BaseException as e:
            logging.exception(e)
            raise MalformedRequestException()

    """
    ==========================Input-purpose-mapping.==========================
    """

    def movement_add_dto_to_movement(self, movement_add_dto):
        try:
            u = Movement()
            u.__dict__ |= movement_add_dto.dict()
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
