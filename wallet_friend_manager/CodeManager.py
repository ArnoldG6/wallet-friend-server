"""
@author: "Miguel González Carvajal".
Github username: "Miguelgonz98".
Contact me via "mgonzalex236@gmail.com".
GPL-3.0 license ©2022
"""
import json
import logging
import random
from hashlib import sha256

from wallet_friend_entities.Entities import User
from wallet_friend_exceptions.WalletFriendExceptions import SingletonObjectException

FILE_NAME = 'Random_Codes.json'


class CodeManager:

    __code_manager_singleton = None  # Singleton CodeManager object

    @staticmethod
    def get_instance():
        """
        Returns:
            CodeManager: the CodeManager class singleton object.
        """
        if CodeManager.__code_manager_singleton is None:
            CodeManager.__code_manager_singleton = CodeManager()
        return CodeManager.__code_manager_singleton

    def __init__(self):
        if CodeManager.__code_manager_singleton is not None:
            raise SingletonObjectException()
        else:
            CodeManager.__code_manager_singleton = self

    def read_codes(self):
        try:
            with open("wallet_friend_manager/"+FILE_NAME, 'r') as openfile:
                code_dictionary = json.load(openfile)
                return code_dictionary
        except Exception as e:  # Any Exception
            logging.exception(f"Reading File Failed. Details: {e}")
            raise e

    @staticmethod
    def calc_random_number():
        return random.randint(10000000, 99999999)

    def add_code(self, user: User):
        try:
            users = self.read_codes()
            random_number = self.calc_random_number()
            while random_number in users.values():
                random_number = self.calc_random_number()
            users[user.username] = sha256(str(random_number).encode('utf-8')).hexdigest()
            with open("wallet_friend_manager/"+FILE_NAME, 'w') as file_object:
                json.dump(users, file_object)
            return random_number
        except Exception as e:  # Any Exception
            logging.exception(f"Writing File Failed. Details: {e}")
            raise e
