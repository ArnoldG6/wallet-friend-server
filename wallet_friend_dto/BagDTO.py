"""
@author: "Miguel González Carvajal".
Github username: "Miguelgonz98".
Contact me via "mgonzalex236@gmail.com".
GPL-3.0 license ©2022
"""
import re
from datetime import datetime
from typing import List

import pydantic
from pydantic import BaseModel, validator

from wallet_friend_dto.HistoricBagMovementDTO import HistoricBagMovementDetailsDTO
from wallet_friend_dto.RoleDTO import RoleDetailsDTO
from wallet_friend_exceptions.HttpWalletFriendExceptions import MalformedRequestException
from wallet_friend_settings import default_password_pattern
from wallet_friend_settings.settings import default_email_pattern
from wallet_friend_tools import check_non_empty_non_spaces_string

"""
=============================================Bag-related DTOs.=============================================
"""

"""
==========================Input DTOs.==========================
"""


class BagAddDTO(BaseModel):
    """
    Input DTO for bag addition.
    """
    owner: str  # id of the account
    balance: float
    goal_balance: float
    end_date: datetime


"""
==========================Output DTOs.==========================
"""


@pydantic.dataclasses.dataclass(frozen=True)
class BagDetailsDTO(BaseModel):
    """
    Output DTO for displaying bag information.
    """
    owner: str  # id of the account
    balance: float
    history: List[HistoricBagMovementDetailsDTO]
    goal_balance: float
    done: bool
    end_date: datetime
