"""
@author: "Miguel González Carvajal".
Github username: "Miguelgonz98".
Contact me via "mgonzalex236@gmail.com".
GPL-3.0 license ©2022
"""
from datetime import datetime
from typing import List, Optional

import pydantic
from pydantic import BaseModel

from wallet_friend_dto.BagMovementDTO import BagMovementDetailsDTO

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
    owner: str  # owner's username
    name: str
    description: str | None = ...
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
    id: int
    owner: int  # id of the account
    creation_datetime: datetime
    name: str
    description: str | None = ...
    amount: float
    available_amount: float
    bag_movements: List[BagMovementDetailsDTO]
