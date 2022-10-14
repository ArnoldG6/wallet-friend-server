"""
@author: "Miguel González Carvajal".
Github username: "Miguelgonz98".
Contact me via "mgonzalex236@gmail.com".
GPL-3.0 license ©2022
"""
from datetime import datetime

import pydantic
from pydantic import BaseModel, validator

from wallet_friend_exceptions.HttpWalletFriendExceptions import MalformedRequestException
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

    @validator("owner")
    def validate_username(cls, v):
        if check_non_empty_non_spaces_string(v):
            return v.lower()
        raise MalformedRequestException("Invalid value in JSON body.")


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
    single_incomes: list
    single_expenses: list
    fixed_incomes: list
    fixed_expenses: list
    bags: list
