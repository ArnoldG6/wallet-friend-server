"""
@author: "Miguel González Carvajal".
Github username: "Miguelgonz98".
Contact me via "mgonzalex236@gmail.com".
GPL-3.0 license ©2022
"""
from datetime import datetime
from typing import List

import pydantic
from pydantic import BaseModel

from wallet_friend_dto.BagMovementDTO import BagMovementDetailsDTO

"""
=============================================FixedMovement-related DTOs.=============================================
"""

"""
==========================Input DTOs.==========================
"""


class FixedMovementAddDTO(BaseModel):
    """
    Input DTO for fixedMovement addition.
    """
    owner: int   # id of the account
    name: str
    description: str | None = ...
    amount: float
    available_amount: float
    temporary_type: str
    repeat_date: datetime | None = ...



"""
==========================Output DTOs.==========================
"""


@pydantic.dataclasses.dataclass(frozen=True)
class FixedMovementDetailsDTO(BaseModel):
    """
    Output DTO for displaying fixedMovement information.
    """
    id: int
    owner: int  # id of the account
    creation_datetime: datetime
    name: str
    description: str | None = ...
    amount: float
    available_amount: float
    bag_movements: list
    temporary_type: str
    repeat_date: datetime | None = ...
