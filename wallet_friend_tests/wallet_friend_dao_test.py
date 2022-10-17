"""
@author: "Miguel González Carvajal".
Github username: "Miguelgonz98".
Contact me via "mgonzalex236@gmail.com".
GPL-3.0 license ©2022
"""
import datetime
import logging

from pydantic.error_wrappers import ValidationError

from wallet_friend_dao import AccountDAO
from wallet_friend_entities.Entities import Account
from wallet_friend_exceptions.HttpWalletFriendExceptions import MalformedRequestException

logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] %(asctime)s - %(message)s')


def test_account_add_dao():
    successful_cases = 0
    account_test = Account()
    account_test.total_balance = 200003.56
    try:
        AccountDAO.get_instance("../wallet_friend_db/config.ini").add(account_test, 'arnold')
        successful_cases += 1
    except MalformedRequestException as e:
        logging.exception(e)
        assert successful_cases != 1
    except Exception as e:
        logging.exception(e)


def account_list_all_dao():
    successful_cases = 0
    account_test = Account()
    account_test.total_balance = 200003.56
    try:
        [print(i) for i in AccountDAO.get_instance("../wallet_friend_db/config.ini").list_all()]
        successful_cases += 1
    except MalformedRequestException as e:
        logging.exception(e)
        assert successful_cases != 1
    except Exception as e:
        logging.exception(e)