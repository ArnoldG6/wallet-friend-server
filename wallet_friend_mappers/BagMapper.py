"""
@author: "Miguel González Carvajal".
Github username: "Miguelgonz98".
Contact me via "mgonzalex236@gmail.com".
GPL-3.0 license ©2022
"""
from sqlalchemy.testing.plugin.plugin_base import logging

from wallet_friend_dto.BagDTO import BagDetailsDTO
from wallet_friend_entities.Entities import Bag
from wallet_friend_exceptions.HttpWalletFriendExceptions import MalformedRequestException
from wallet_friend_exceptions.WalletFriendExceptions import SingletonObjectException
from wallet_friend_mappers import HistoricBagMovementMapper
from wallet_friend_mappers.Mapper import Mapper


class BagMapper(Mapper):
    """
    BagMapper translate BagDTO objects into Bag objects and vice-versa.
    """
    bag_mapper_singleton = None  # Singleton BagMapper object

    @staticmethod
    def get_instance():
        """
        Returns:
            bag_mapper_singleton: the BagMapper's class singleton object.
        """
        if BagMapper.bag_mapper_singleton is None:
            BagMapper.bag_mapper_singleton = BagMapper()
        return BagMapper.bag_mapper_singleton

    def __init__(self):
        super().__init__()
        if BagMapper.bag_mapper_singleton is not None:
            raise SingletonObjectException()
        else:
            BagMapper.bag_mapper_singleton = self

    """
    ==========================Outer-purpose-mapping.==========================
    """

    def bag_to_bag_details_dto(self, u):
        try:
            bag_d = u.__dict__
            bag_d["history"] = HistoricBagMovementMapper.get_instance(). \
                historic_bag_movement_list_to_historic_bag_movement_details_dto_list(u.history)
            return BagDetailsDTO(**bag_d)
        except ValueError as e:
            logging.exception(e)
            raise MalformedRequestException(str(e))
        except MalformedRequestException as e:
            logging.exception(e)
            raise e
        except BaseException as e:
            logging.exception(e)
            raise MalformedRequestException()

    def bag_list_to_bag_details_dto_list(self, bag_list):
        """
        Params:
            bag_list: List of Bag objects to be translated.
        Returns:
                A list of BagDetailsDTO objects.
            """
        try:
            return [self.bag_to_bag_details_dto(r) for r in bag_list]
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

    def bag_add_dto_to_bag(self, bag_add_dto):
        try:
            u = Bag()
            u.__dict__ |= bag_add_dto.dict()
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
