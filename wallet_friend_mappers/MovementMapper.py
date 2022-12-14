"""
@author: "Miguel González Carvajal".
Github username: "Miguelgonz98".
Contact me via "mgonzalex236@gmail.com".
GPL-3.0 license ©2022
"""
import logging

from wallet_friend_dto.MovementDTO import MovementDetailsDTO
from wallet_friend_entities.Entities import Movement
from wallet_friend_exceptions.HttpWalletFriendExceptions import MalformedRequestException
from wallet_friend_exceptions.WalletFriendExceptions import SingletonObjectException
from wallet_friend_mappers.BagMovementMapper import BagMovementMapper
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

    def movement_to_movement_details_dto(self, movement):
        try:
            movement_d = movement.__dict__
            movement_d["owner"] = movement.account_id
            movement_d["bag_movements"] = BagMovementMapper.get_instance(). \
                bag_movement_list_to_bag_movement_details_dto_list(movement.bag_movements)
            # if not movement_d.get("description", None):
            #     movement.description = None
            return MovementDetailsDTO(**movement_d)

        except ValueError as e:
            logging.exception(e)
            raise MalformedRequestException(str(e))
        except MalformedRequestException as e:
            logging.exception(e)
            raise e
        except BaseException as e:
            logging.exception(e)
            raise MalformedRequestException()

    def movement_list_to_movement_details_dto_list(self, movement_list):
        """
        Params:
            movement_list: List of Movements objects to be translated.
        Returns:
            A list of MovementDetailsDTO objects.
        """
        try:
            return [self.movement_to_movement_details_dto(m) for m in movement_list]
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

    def movement_add_dto_to_movement(self, movement_add_dto):
        try:
            u = Movement()
            u.__dict__ |= movement_add_dto.dict()
            # if not u.__dict__.get("description", None):
            #    u.description = None
            u.__dict__["account_id"] = u.__dict__["owner"]
            del u.__dict__["owner"]
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
