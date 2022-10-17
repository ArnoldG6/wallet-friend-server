"""
@author: "Arnoldo J. González Quesada".
Github username: "ArnoldG6".
Contact me via "arnoldgq612@gmail.com".
GPL-3.0 license ©2022
"""
import logging

from wallet_friend_dto import UserAuthDTO
from wallet_friend_dto.AccountDTO import AccountAddDTO
from wallet_friend_exceptions.HttpWalletFriendExceptions import MalformedRequestException

logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] %(asctime)s - %(message)s')

"""
=============================================User-related DTOs.=============================================
"""


def test_user_auth_dto_1():
    try:
        successful_cases = 0
        samples = [("23", None),
                   ("23", ""),
                   ("23", "xd"),
                   ("", "a"),
                   ("23", 5),
                   ("23", None),
                   ("", "")
                   ]
        # Only two cases are expected to pass
        for (a, b) in samples:
            try:
                logging.info(f"({a},{b}): {UserAuthDTO(username=a, password=b).json()}")
                successful_cases += 1
            except MalformedRequestException as e:
                logging.exception(e)
        assert successful_cases != 2
    except Exception as e:
        logging.exception(e)


def test_user_details_dto_1():
    try:
        pass
    except Exception as e:
        logging.exception(e)


def test_account_add_dto():
    try:
        '''
        owner: str  # username of the owner
        total_balance: float
        '''

        successful_cases = 0
        samples = [
            ("manuelg569", 291000.54),
            ("arnoldgq612", 16500.8888),
            (None, 28504),
            ("Luis", None),
            ("", 0)
        ]
        # Only two cases are expected to pass
        for index in range(len(samples)):
            for key in samples[index]:
                print(samples[index][key])
        for (a,b) in samples:
            try:
                print(AccountAddDTO(owner=a, total_balance=b).dict())
                logging.info(f"({a},{b}): {AccountAddDTO(owner=a, total_balance=b).json()}")
                successful_cases += 1
            except MalformedRequestException as e:
                logging.exception(e)
        assert successful_cases != 2
    except Exception as e:
        logging.exception(e)
