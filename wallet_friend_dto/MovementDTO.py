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

from wallet_friend_dto import BagMovementDTO
from wallet_friend_dto.RoleDTO import RoleDetailsDTO
from wallet_friend_exceptions.HttpWalletFriendExceptions import MalformedRequestException
from wallet_friend_settings import default_password_pattern
from wallet_friend_settings.settings import default_email_pattern
from wallet_friend_tools import check_non_empty_non_spaces_string

"""
=============================================Movement-related DTOs.=============================================
"""

"""
==========================Input DTOs.==========================
"""


class MovementAddDTO(BaseModel):
    """
    Input DTO for movement addition.
    """
    owner: str  # id of the account
    name: str
    description: str
    amount: float
    available_amount: float


"""
==========================Output DTOs.==========================
"""


@pydantic.dataclasses.dataclass(frozen=True)
class MovementDetailsDTO(BaseModel):
    """
    Output DTO for displaying movement information.
    """
    owner: str  # id of the account
    creation_datetime: datetime
    name: str
    description: str
    amount: int
    available_amount: int
    bagMovements: list
