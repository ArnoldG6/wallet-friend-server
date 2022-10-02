"""
@author: "Arnoldo J. González Quesada".
Github username: "ArnoldG6".
Contact me via "arnoldgq612@gmail.com".
GPL-3.0 license ©2022
"""
import logging

from sqlalchemy import create_engine
from sqlalchemy.exc import PendingRollbackError
from sqlalchemy.orm import sessionmaker

from wallet_friend_db import DbSettingsParser


class DAO:
    db_settings_path = "wallet_friend_db/config.ini"

    def __init__(self):
        self.__session = None
        self.__default_profile = "local_postgresql"
        self.__db_settings = DbSettingsParser.get_instance().read_db_config(filename=DAO.db_settings_path,
                                                                            section=self.__default_profile)
        self.__db_string = f"postgresql://{self.__db_settings['user']}:{self.__db_settings['password']}@{self.__db_settings['host']}:{self.__db_settings['port']}/{self.__db_settings['database']}"
        self.__engine = create_engine(self.__db_string)

    @staticmethod
    def get_instance():
        pass

    def get_db_settings(self):
        return self.__db_settings

    def create_session(self):
        try:
            return sessionmaker(bind=self.__engine)()  # Session shall be closed from outside
        except BaseException as e:
            logging.exception(e)
