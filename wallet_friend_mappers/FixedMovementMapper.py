"""
@author: "Miguel González Carvajal".
Github username: "Miguelgonz98".
Contact me via "mgonzalex236@gmail.com".
GPL-3.0 license ©2022
"""
import logging

from wallet_friend_dto.FixedMovementDTO import FixedMovementDetailsDTO
from wallet_friend_entities.Entities import FixedMovement, Movement
from wallet_friend_exceptions.HttpWalletFriendExceptions import MalformedRequestException
from wallet_friend_exceptions.WalletFriendExceptions import SingletonObjectException
from wallet_friend_mappers.BagMovementMapper import BagMovementMapper
from wallet_friend_mappers.Mapper import Mapper


class FixedMovementMapper(Mapper):
    """
    FixedMovementMapper translate FixedMovementDTO objects into FixedMovement objects and vice-versa.
    """
    fixed_movement_mapper_singleton = None  # Singleton FixedMovementMapper object

    @staticmethod
    def get_instance():
        """
        Returns:
            movement_mapper_singleton: the MovementMapper's class singleton object.
        """
        if FixedMovementMapper.fixed_movement_mapper_singleton is None:
            FixedMovementMapper.fixed_movement_mapper_singleton = FixedMovementMapper()
        return FixedMovementMapper.fixed_movement_mapper_singleton

    def __init__(self):
        super().__init__()
        if FixedMovementMapper.fixed_movement_mapper_singleton is not None:
            raise SingletonObjectException()
        else:
            FixedMovementMapper.fixed_movement_mapper_singleton = self

    """
    ==========================Outer-purpose-mapping.==========================
    """

    def fixed_movement_to_fixed_movement_details_dto(self, fixed_movement):
        try:

            fixed_movement_d = fixed_movement.__dict__
            fixed_movement_d["bag_movements"] = BagMovementMapper.get_instance(). \
                bag_movement_list_to_bag_movement_details_dto_list(fixed_movement.bag_movements)
            fixed_movement.owner = fixed_movement.account_id
            fixed_movement.temporary_type = "Monthly"
            if not fixed_movement_d.get("repeat_date", None):
                fixed_movement.repeat_date = None
            return FixedMovementDetailsDTO(**fixed_movement_d)

        except MalformedRequestException as e:
            logging.exception(e)
            raise e
        except BaseException as e:
            logging.exception(e)
            raise MalformedRequestException()

    def fixed_movement_list_to_fixed_movement_details_dto_list(self, fixed_movement_list):
        """
        Params:
            fixed_movement_list: List of FixedMovements objects to be translated.
        Returns:
            A list of FixedMovementDetailsDTO objects.
        """
        try:
            return [self.fixed_movement_to_fixed_movement_details_dto(r) for r in fixed_movement_list]
        except MalformedRequestException as e:
            logging.exception(e)
            raise e

    """
    ==========================Input-purpose-mapping.==========================
    """

    def fixed_movement_add_dto_to_fixed_movement(self, fixed_movement_add_dto):
        try:
            u = FixedMovement()
            u.__dict__ |= fixed_movement_add_dto.dict()
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
