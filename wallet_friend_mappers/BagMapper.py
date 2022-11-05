"""
@author: "Miguel González Carvajal".
Github username: "Miguelgonz98".
Contact me via "mgonzalex236@gmail.com".
GPL-3.0 license ©2022
"""
import logging
from datetime import datetime
from wallet_friend_dto.BagDTO import BagDetailsDTO
from wallet_friend_entities.Entities import Bag
from wallet_friend_exceptions.HttpWalletFriendExceptions import MalformedRequestException
from wallet_friend_exceptions.WalletFriendExceptions import SingletonObjectException
from wallet_friend_mappers.HistoricBagMovementMapper import HistoricBagMovementMapper
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

    def bag_to_bag_details_dto(self, bag):
        try:
            bag_d = bag.__dict__
            bag_d["history"] = HistoricBagMovementMapper.get_instance(). \
                historic_bag_movement_list_to_historic_bag_movement_details_dto_list(bag.history)
            bag_d["owner"] = bag.account_id
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
            u.__dict__["account_id"] = int(u.__dict__["owner"])
            del u.__dict__["owner"]
            # u.__dict__["end_date"] = datetime.strptime(u.__dict__["end_date"], '%d/%m/%Y')
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
