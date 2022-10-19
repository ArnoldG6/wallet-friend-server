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
    name: str
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
    id: int
    owner: str  # id of the account
    name: str
    balance: float
    history: list
    goal_balance: float
    done: bool
    end_date: datetime
