"""
@author: "Miguel González Carvajal".
Github username: "Miguelgonz98".
Contact me via "mgonzalex236@gmail.com".
GPL-3.0 license ©2022
"""
from datetime import datetime

import pydantic
from pydantic import BaseModel

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
    owner: str  # id of the account
    name: str
    description: str
    amount: float
    available_amount: float
    temporary_type: str
    repeat_date: datetime


"""
==========================Output DTOs.==========================
"""


@pydantic.dataclasses.dataclass(frozen=True)
class FixedMovementDetailsDTO(BaseModel):
    """
    Output DTO for displaying fixedMovement information.
    """
    owner: str  # id of the account
    creation_datetime: datetime
    name: str
    description: str
    amount: float
    available_amount: float
    bagMovements: list
    temporary_type: str
    repeat_date: datetime
