"""
@author: "Arnoldo J. González Quesada".
Github username: "ArnoldG6".
Contact me via "arnoldgq612@gmail.com".
GPL-3.0 license ©2022
"""
from datetime import datetime
import logging

from sqlalchemy import create_engine

from wallet_friend_dao import UserDAO
from wallet_friend_dao.RoleDAO import RoleDAO
from wallet_friend_db import DbSettingsParser
from wallet_friend_entities.Entities import updated_base, User, Account, Movement, FixedMovement, TemporaryType, Bag, \
    BagMovement, HistoricBagMovement
from wallet_friend_mappers.AccountMapper import AccountMapper
from wallet_friend_mappers.BagMapper import BagMapper
from wallet_friend_mappers.BagMovementMapper import BagMovementMapper
from wallet_friend_mappers.FixedMovementMapper import FixedMovementMapper
from wallet_friend_mappers.MovementMapper import MovementMapper


class DatabaseGenerator:

    def generate(self):
        """
        :return: None
        generate method drops and creates all tables based on Entities.py file of the present project.
        """
        # Warning!: Run only once when you need to create the DB
        db_settings_path = "../wallet_friend_db/config.ini"
        default_profile = "local_postgresql"
        # default_profile = "cloud_postgresql"
        db_settings = DbSettingsParser.get_instance().read_db_config(filename=db_settings_path,
                                                                     section=default_profile)
        db_string = f"postgresql://{db_settings['user']}:{db_settings['password']}@{db_settings['host']}:{db_settings['port']}/{db_settings['database']}"
        engine = create_engine(db_string)
        updated_base.metadata.drop_all(bind=engine)
        updated_base.metadata.create_all(engine, updated_base.metadata.tables.values())
        """
        Inits default auth data
        """
        # ======================== SO Of User-Role data ========================
        user = User()
        user.__dict__ |= {
            "username": "arnold",
            "email": "arnoldgq612@gmail.com",
            "pwd_hash": "8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918",
            "first_name": "Arnold",
            "last_name": "González",
            "enabled": True,
            "creation_datetime": datetime.now(),
            "token": None
        }
        session = UserDAO.get_instance(db_settings_path).create_session()
        role = RoleDAO.get_instance(db_settings_path).export_default_client_role()
        session.object_session(role)
        session.add(role)
        # session.merge(user)
        user.roles = [role]
        role.users.append(user)
        session.add(user)
        # ======================== EO Of User-Role data ========================
        # ======================== SO Of Account data ========================
        account = Account(
            creation_datetime=datetime.now(),
            total_balance=0.0,
            owner_id=user.id,
            owner=user
        )

        session.object_session(account)
        session.add(account)
        try:
            session.flush()
            # ======================== EO Of Account data ========================
            # ======================== SO Of Movements data ========================
            account.movements = [
                Movement(
                    creation_datetime=datetime.now(),
                    account_id=account.id,
                    amount=-666.0,
                    available_amount=0.0,
                    name="Cerveza chafa",
                    description="algo"
                ),
                Movement(
                    creation_datetime=datetime.now(),
                    account_id=account.id,
                    amount=5000.0,
                    available_amount=0.0,
                    name="Billete encontrado",
                    description="algo"
                )
            ]
            account.total_balance = account.movements[0].amount + account.movements[1].amount
            session.flush()
            # print(AccountMapper.get_instance().account_to_account_details_dto(account))
            # print(account)
            # print(MovementMapper.get_instance().movement_to_movement_details_dto(account.movements[0]))
            # print(MovementMapper.get_instance().movement_list_to_movement_details_dto_list(account.movements))
            # ======================== EO Of Movements data ========================
            # ======================== SO Of FixedMovements data ========================
            account.fixed_movements = [
                FixedMovement(
                    creation_datetime=datetime.now(),
                    account_id=account.id,
                    amount=1200000.0,
                    available_amount=1200000.0,
                    name="Salario",
                    description="algo",
                    temporary_type=str(TemporaryType.monthly.value),
                ),
                FixedMovement(
                    creation_datetime=datetime.now(),
                    account_id=account.id,
                    amount=-10000.0,
                    available_amount=0.0,
                    name="Factura electricidad",
                    description="algo",
                    temporary_type=str(TemporaryType.monthly.value),
                )
            ]
            # print(FixedMovementMapper.get_instance().
            #      fixed_movement_to_fixed_movement_details_dto(account.fixed_movements[0]))
            # print(FixedMovementMapper.get_instance().
            #       fixed_movement_list_to_fixed_movement_details_dto_list(account.fixed_movements))
            # ======================== EO Of FixedMovements data ========================
            # ======================== SO Of Bag data ========================
            account.bags = [
                Bag(creation_datetime=datetime.now(),
                    name="My bag",
                    account_id=account.id,
                    balance=5000.0,
                    goal_balance=40000.0,
                    done=False,
                    end_date=datetime.strptime('21/01/24 11:04:19', '%d/%m/%y %H:%M:%S')
                    )
            ]
            session.flush()
            # print(BagMapper.get_instance().bag_list_to_bag_details_dto_list(account.bags))
            # ======================== EO Of Bag data ========================
            # ======================== SO Of BagMovement data ========================
            bag = account.bags[0]
            # movements = account.movements
            # print(BagMapper.get_instance().bag_to_bag_details_dto(bag))
            # print(BagMapper.get_instance().bag_list_to_bag_details_dto_list(account.bags))
            account.movements[1].bag_movements.append(BagMovement(creation_datetime=datetime.now(),
                                                                  bag_id=bag.id,
                                                                  bag=bag,
                                                                  amount=5000.0))
            # print(account.movements[0].bag_movements) print(BagMovementMapper.get_instance(
            # ).bag_movement_list_to_bag_movement_details_dto_list(account.movements[0].bag_movements))
            # print(AccountMapper.get_instance().account_to_account_details_dto(account))

            bag.history.append(HistoricBagMovement(creation_datetime=datetime.now(),
                                                   amount=5000.0,
                                                   origin=account.movements[1].id))

            print(bag.history[0].amount)
            session.flush()
            # ======================== EO Of BagMovement data ========================
            session.commit()
            session.close()

        except BaseException as e:
            logging.exception(e)


DatabaseGenerator().generate()
