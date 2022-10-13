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
==========================Output DTOs.==========================
"""


@pydantic.dataclasses.dataclass(frozen=True)
class BagMovementDetailsDTO(BaseModel):
    """
    Output BagMovement DTO
    """
    creation_datetime: datetime
    bag: object
    amount: float
