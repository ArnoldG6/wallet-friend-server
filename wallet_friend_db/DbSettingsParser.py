"""
@author: "Arnoldo J. González Quesada".
Github username: "ArnoldG6".
Contact me via "arnoldgq612@gmail.com".
GPL-3.0 license ©2022
"""
from __future__ import annotations

from configparser import ConfigParser


class DbSettingsParser:
    """
    DbSettingsParser class is in charge to read .ini file for DB configuration.
    """
    __db_settings_parser_singleton = None

    @staticmethod
    def get_instance() -> DbSettingsParser:
        """
        return:
            DbSettingsParser: the DbSettingsParser class singleton object.
        """
        if DbSettingsParser.__db_settings_parser_singleton is None:
            DbSettingsParser.__db_settings_parser_singleton = DbSettingsParser()
        return DbSettingsParser.__db_settings_parser_singleton

    def __init__(self):
        if DbSettingsParser.__db_settings_parser_singleton is not None:
            raise Exception("Singleton Class Exception")
        else:
            DbSettingsParser.__db_settings_parser_singleton = self

    def read_db_config(self, filename='/config.ini', section='local_postgresql') -> dict:

        parser = ConfigParser()
        parser.read(filename)
        db_settings_dict = {}
        if parser.has_section(section):
            items = parser.items(section)
            for item in items:
                db_settings_dict[item[0]] = item[1]
            return db_settings_dict
        raise Exception(f"Section: '{section}' not found in '{filename}'.")
