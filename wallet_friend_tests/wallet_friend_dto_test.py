"""
@author: "Arnoldo J. González Quesada".
Github username: "ArnoldG6".
Contact me via "arnoldgq612@gmail.com".
GPL-3.0 license ©2022
"""
import datetime
import json
import logging

from pydantic.error_wrappers import ValidationError

from wallet_friend_dto import UserAuthDTO
from wallet_friend_entities import User, Permission

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
                # print(UserAuthDTO(username=a, password=b).dict())
                logging.info(f"({a},{b}): {UserAuthDTO(username=a, password=b).json()}")
                successful_cases += 1
            except ValidationError as e:
                print(e)
        assert successful_cases != 2
    except Exception as e:
        logging.exception(e)


def test_user_details_dto_1():
    try:
        pass
    except Exception as e:
        logging.exception(e)
