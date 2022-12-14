"""
@author: "Miguel González Carvajal".
Github username: "Miguelgonz98".
Contact me via "mgonzalex236@gmail.com".
GPL-3.0 license ©2022
"""
import logging

from wallet_friend_dto.HistoricBagMovementDTO import HistoricBagMovementDetailsDTO
from wallet_friend_exceptions.HttpWalletFriendExceptions import MalformedRequestException
from wallet_friend_exceptions.WalletFriendExceptions import SingletonObjectException
from wallet_friend_mappers.Mapper import Mapper


class HistoricBagMovementMapper(Mapper):
    """
    HistoricBagMovementMapper translate HistoricBagMovementDTO objects into HistoricBagMovement objects and vice-versa.
    """
    historic_bag_movement_mapper_singleton = None  # Singleton HistoricBagMovementMapper object

    @staticmethod
    def get_instance():
        """
        Returns:
            historic_bag_movement_mapper_singleton: the HistoricBagMovementMapper's class singleton object.
        """
        if HistoricBagMovementMapper.historic_bag_movement_mapper_singleton is None:
            HistoricBagMovementMapper.historic_bag_movement_mapper_singleton = HistoricBagMovementMapper()
        return HistoricBagMovementMapper.historic_bag_movement_mapper_singleton

    def __init__(self):
        super().__init__()
        if HistoricBagMovementMapper.historic_bag_movement_mapper_singleton is not None:
            raise SingletonObjectException()
        else:
            HistoricBagMovementMapper.historic_bag_movement_mapper_singleton = self

    """
    ==========================Outer-purpose-mapping.==========================
    """

    def historic_bag_movement_to_historic_bag_movement_details_dto(self, u):
        try:
            historic_bag_movement_d = u.__dict__
            #if not u.__dict__.get("description",None):
            #    u.description = None
            return HistoricBagMovementDetailsDTO(**historic_bag_movement_d)
        except ValueError as e:
            logging.exception(e)
            raise MalformedRequestException(str(e))
        except MalformedRequestException as e:
            logging.exception(e)
            raise e
        except BaseException as e:
            logging.exception(e)
            raise MalformedRequestException()

    def historic_bag_movement_list_to_historic_bag_movement_details_dto_list(self, historic_bag_movement_list):
        try:
            return [self.historic_bag_movement_to_historic_bag_movement_details_dto(r) for \
                    r in historic_bag_movement_list]
        except ValueError as e:
            logging.exception(e)
            raise MalformedRequestException(str(e))
        except MalformedRequestException as e:
            logging.exception(e)
            raise e
        except BaseException as e:
                logging.exception(e)
                raise MalformedRequestException()

