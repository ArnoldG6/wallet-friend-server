"""
@author: "Arnoldo J. González Quesada".
Github username: "ArnoldG6".
Contact me via "arnoldgq612@gmail.com".
GPL-3.0 license ©2022
"""

from wallet_friend_db import DbSettingsParser
from wallet_friend_entities.Entities import updated_base
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


DatabaseGenerator().generate()
