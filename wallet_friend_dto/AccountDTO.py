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

from wallet_friend_dto.BagDTO import BagDetailsDTO
from wallet_friend_dto.FixedMovementDTO import FixedMovementDetailsDTO
from wallet_friend_dto.MovementDTO import MovementDetailsDTO
from wallet_friend_dto.RoleDTO import RoleDetailsDTO
from wallet_friend_exceptions.HttpWalletFriendExceptions import MalformedRequestException
from wallet_friend_settings import default_password_pattern
from wallet_friend_settings.settings import default_email_pattern
from wallet_friend_tools import check_non_empty_non_spaces_string

"""
=============================================Account-related DTOs.=============================================
"""

"""
==========================Input DTOs.==========================
"""


class AccountAddDTO(BaseModel):
    """
    Input DTO for account addition.
    """
    owner: str  # username of the owner
    total_balance: float


"""
==========================Output DTOs.==========================
"""


@pydantic.dataclasses.dataclass(frozen=True)
class AccountDetailsDTO(BaseModel):
    """
    Output DTO for displaying account information.
    """
    id: str
    owner: str  # username of the owner
    creation_datetime: datetime
    total_balance: float
    single_incomes: List[MovementDetailsDTO]
    single_expenses: List[MovementDetailsDTO]
    fixed_incomes: List[FixedMovementDetailsDTO]
    fixed_expenses: List[FixedMovementDetailsDTO]
    bags: List[BagDetailsDTO]
