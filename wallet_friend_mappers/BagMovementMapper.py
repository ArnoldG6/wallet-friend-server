"""
@author: "Miguel González Carvajal".
Github username: "Miguelgonz98".
Contact me via "mgonzalex236@gmail.com".
GPL-3.0 license ©2022
"""
from sqlalchemy.testing.plugin.plugin_base import logging

from wallet_friend_dto.BagMovementDTO import BagMovementDetailsDTO
from wallet_friend_exceptions.HttpWalletFriendExceptions import MalformedRequestException
from wallet_friend_exceptions.WalletFriendExceptions import SingletonObjectException
from wallet_friend_mappers import BagMapper
from wallet_friend_mappers.Mapper import Mapper


class BagMovementMapper(Mapper):
    """
    BagMovementMapper translate BagMovementDTO objects into BagMovement objects and vice-versa.
    """
    bag_movement_mapper_singleton = None  # Singleton BagMovementMapper object

    @staticmethod
    def get_instance():
        """
        Returns:
            bag_movement_mapper_singleton: the BagMovementMapper's class singleton object.
        """
        if BagMovementMapper.bag_movement_mapper_singleton is None:
            BagMovementMapper.bag_movement_mapper_singleton = BagMovementMapper()
        return BagMovementMapper.bag_movement_mapper_singleton

    def __init__(self):
        super().__init__()
        if BagMovementMapper.bag_movement_mapper_singleton is not None:
            raise SingletonObjectException()
        else:
            BagMovementMapper.bag_movement_mapper_singleton = self

    """
    ==========================Outer-purpose-mapping.==========================
    """

    def bag_movement_to_bag_movement_details_dto(self, u):
        try:
            bag_movement_d = u.__dict__
            bag_movement_d["bag"] = BagMapper.get_instance().bag_to_bag_details_dto(u.bag)
            return BagMovementDetailsDTO(**bag_movement_d)

        except MalformedRequestException as e:
            logging.exception(e)
            raise e
        except BaseException as e:
            logging.exception(e)
            raise MalformedRequestException()
