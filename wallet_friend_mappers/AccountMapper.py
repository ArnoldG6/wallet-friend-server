"""
@author: "Miguel González Carvajal".
Github username: "Miguelgonz98".
Contact me via "mgonzalex236@gmail.com".
GPL-3.0 license ©2022
"""
import logging

from wallet_friend_dto.AccountDTO import AccountDetailsDTO
from wallet_friend_entities.Entities import Account
from wallet_friend_exceptions.HttpWalletFriendExceptions import MalformedRequestException
from wallet_friend_exceptions.WalletFriendExceptions import SingletonObjectException
from wallet_friend_mappers.MovementMapper import MovementMapper
from wallet_friend_mappers.FixedMovementMapper import FixedMovementMapper
from wallet_friend_mappers.BagMapper import BagMapper
from wallet_friend_mappers.Mapper import Mapper


class AccountMapper(Mapper):
    """
    AccountMapper translate AccountDTO objects into Account objects and vice-versa.
    """
    account_mapper_singleton = None  # Singleton AccountMapper object

    @staticmethod
    def get_instance():
        """
        Returns:
            account_mapper_singleton: the AccountMapper's class singleton object.
        """
        if AccountMapper.account_mapper_singleton is None:
            AccountMapper.account_mapper_singleton = AccountMapper()
        return AccountMapper.account_mapper_singleton

    def __init__(self):
        super().__init__()
        if AccountMapper.account_mapper_singleton is not None:
            raise SingletonObjectException()
        else:
            AccountMapper.account_mapper_singleton = self

    """
    ==========================Outer-purpose-mapping.==========================
    """

    def account_to_account_details_dto(self, account: Account):
        try:
            single_incomes = []
            single_expenses = []
            fixed_incomes = []
            fixed_expenses = []
            for m in account.movements:
                if m not in account.fixed_movements:
                    if m.amount > 0:  # if it is positive
                        single_incomes.append(m)
                    elif m.amount < 0:
                        single_expenses.append(m)

            for fm in account.fixed_movements:
                if fm.amount > 0:  # if it is positive
                    fixed_incomes.append(fm)
                elif fm.amount < 0:
                    fixed_expenses.append(fm)
            result = {
                "id": account.id,
                "owner": account.owner.username,
                "creation_datetime": account.creation_datetime,
                "total_balance": account.total_balance,
                "single_incomes": MovementMapper.get_instance().
                movement_list_to_movement_details_dto_list(single_incomes),
                "single_expenses": MovementMapper.get_instance().
                movement_list_to_movement_details_dto_list(single_expenses),
                "fixed_incomes": FixedMovementMapper.get_instance().
                fixed_movement_list_to_fixed_movement_details_dto_list(fixed_incomes),
                "fixed_expenses": FixedMovementMapper.get_instance().
                fixed_movement_list_to_fixed_movement_details_dto_list(fixed_expenses),
                "bags": BagMapper.get_instance().bag_list_to_bag_details_dto_list(account.bags)
            }
            return AccountDetailsDTO(**result)
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

    def account_add_dto_to_account(self, account_add_dto):
        try:
            u = Account()
            u.__dict__ |= account_add_dto.dict()
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
