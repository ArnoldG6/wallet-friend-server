"""
@author: "Arnoldo J. González Quesada".
Github username: "ArnoldG6".
Contact me via "arnoldgq612@gmail.com".
GPL-3.0 license ©2022
"""
import datetime

from wallet_friend_dao import UserDAO
from wallet_friend_dao.PermissionDAO import ClientPermission
from wallet_friend_dao.RoleDAO import ClientRole, RoleDAO
from wallet_friend_db import DbSettingsParser
from wallet_friend_entities.Entities import updated_base, Role, Permission, User
from sqlalchemy import create_engine


class DatabaseGenerator:

    def generate(self):
        """
        :return: None
        generate method drops and creates all tables based on Entities.py file of the present project.
        """
        # Warning!: Run only once when you need to create the DB
        db_settings_path = "../wallet_friend_db/config.ini"
        default_profile = "local_postgresql"
        db_settings = DbSettingsParser.get_instance().read_db_config(filename=db_settings_path,
                                                                     section=default_profile)
        db_string = f"postgresql://{db_settings['user']}:{db_settings['password']}@{db_settings['host']}:{db_settings['port']}/{db_settings['database']}"
        engine = create_engine(db_string)
        updated_base.metadata.drop_all(bind=engine)
        updated_base.metadata.create_all(engine, updated_base.metadata.tables.values())
        """
        Inits default auth data
        """
        user = User()
        user.__dict__ |= {
            "username": "arnold",
            "email": "arnoldgq612@gmail.com",
            "pwd_hash": "8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918",
            "first_name": "Arnold",
            "last_name": "González",
            "enabled": True,
            "creation_datetime": datetime.datetime.now(),
            "token": None
        }
        session = UserDAO.get_instance("../wallet_friend_db/config.ini").create_session()
        role = RoleDAO.get_instance("../wallet_friend_db/config.ini").export_default_client_role()
        session.object_session(role)
        session.add(role)
        # session.merge(user)
        user.roles = [role]
        role.users.append(user)
        session.add(user)
        session.commit()
        session.close()


DatabaseGenerator().generate()
