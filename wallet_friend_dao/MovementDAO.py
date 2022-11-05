"""
@author: "Miguel González Carvajal".
Github username: "Miguelgonz98".
Contact me via "mgonzalex236@gmail.com".
GPL-3.0 license ©2022
"""
import datetime
from decimal import Decimal

from sqlalchemy.exc import NoResultFound
import logging

from wallet_friend_exceptions.WalletFriendExceptions import SingletonObjectException
from .DAO import DAO
from wallet_friend_entities.Entities import Movement, Account, Bag, BagMovement, HistoricBagMovement
from wallet_friend_exceptions.HttpWalletFriendExceptions import NonExistentRecordException, MalformedRequestException, \
    ExistentRecordException


class MovementDAO(DAO):
    """
    DBHandler class  manages the mqd_db queries in order to use CRUD methods.
    """
    __movement_dao_singleton = None  # Singleton AccountDAO object

    @staticmethod
    def get_instance():
        """
        Returns:
            MovementDAO: the MovementDAO class singleton object.
        """
        if MovementDAO.__movement_dao_singleton is None:
            MovementDAO.__movement_dao_singleton = MovementDAO()
        return MovementDAO.__movement_dao_singleton

    def __init__(self):
        super().__init__()
        if MovementDAO.__movement_dao_singleton is not None:
            raise SingletonObjectException()
        else:
            MovementDAO.__movement_dao_singleton = self

    def list_all(self):
        try:
            session = self.create_session()
            result = session.query(Movement).all()
            if result is None:
                raise NonExistentRecordException()
            return result
        except BaseException as e:
            logging.exception(f"DB Connection failed. Details: {e}")
            raise e

    def add(self, new_movement: Movement):
        session = None
        a = None
        try:
            if not new_movement:
                raise MalformedRequestException("Invalid parameter 'new_movement' exception")
            account_id = new_movement.account_id
            session = self.create_session()
            try:
                a = session.query(Account).filter(Account.id == account_id).one()
            except NoResultFound as e:
                raise NonExistentRecordException("This record is not existent")
            new_movement.account = a
            new_movement.account_id = a.id
            a.total_balance = Decimal(float(a.total_balance) + new_movement.amount)
            new_movement.creation_datetime = datetime.datetime.now()
            # new_movement.bag_movements = []
            session.add(new_movement)
            session.commit()
        except ExistentRecordException as e:
            logging.exception(e)
            raise e
        except Exception as e:  # Any other Exception
            logging.exception(f"DB Connection failed. Details: {e}")
            raise e
        finally:
            if session:
                session.close()

    def update(self, update_movement: Movement):
        try:
            session = self.create_session()
            filters = (Movement.id == update_movement.id)
            movement = session.query(Movement).filter(filters).one()
            if movement is None:
                raise NonExistentRecordException()
            else:
                movement.amount = update_movement.amount
                movement.available_amount = update_movement.available_amount
                movement.name = update_movement.name
                movement.description = update_movement.description
                # Pending updates
                session.commit()
        except BaseException as e:
            logging.exception(f"DB Connection failed. Details: {e}")
            raise e

    def delete(self, movement_id: int):
        try:
            session = self.create_session()
            try:
                movement = session.query(Movement).filter((Movement.id == movement_id)).one()
                session.delete(movement)
                session.commit()
            except NoResultFound as e:
                raise NonExistentRecordException('movement_id not found')

        except BaseException as e:
            logging.exception(f"DB Connection failed. Details: {e}")
            raise e

    def add_bag_movement_to_movement(self, movement_id: int, bag_id: int, bag_movement_amount: float):
        try:
            session = self.create_session()
            movement = None
            bag = None
            try:
                movement = session.query(Movement).filter((Movement.id == movement_id)).one()
            except NoResultFound as e:
                raise NonExistentRecordException('movement_id not found')
            try:
                bag = session.query(Bag).filter((Bag.id == bag_id)).one()
            except NoResultFound as e:
                raise NonExistentRecordException('movement_id not found')
            bag_movement = BagMovement(
                creation_datetime=datetime.datetime.now(),
                bag_id=bag.id,
                bag=bag,
                movement_id=movement.id,
                amount=bag_movement_amount
            )
            account = bag.account
            account.total_balance = Decimal(float(account.total_balance) + bag_movement_amount)
            bag.balance = Decimal(float(bag.balance)+bag_movement_amount)
            if bag.balance > bag.goal_balance:
                bag.done = True
            session.add(bag_movement)
            session.flush()
            historic_bag_movement = HistoricBagMovement(
                creation_datetime=datetime.datetime.now(),
                amount=bag_movement_amount,
                origin=movement.id,
                bag_id=bag.id,
                bag=bag
            )

            session.add(historic_bag_movement)
            session.commit()

        except BaseException as e:
            logging.exception(f"DB Connection failed. Details: {e}")
            raise e
