"""
@author: "Miguel González Carvajal".
Github username: "Miguelgonz98".
Contact me via "mgonzalex236@gmail.com".
GPL-3.0 license ©2022
"""
from datetime import datetime

import pydantic
from pydantic import BaseModel

from wallet_friend_dto.BagDTO import BagDetailsDTO

"""
==========================Output DTOs.==========================
"""


@pydantic.dataclasses.dataclass(frozen=True)
class BagMovementDetailsDTO(BaseModel):
    """
    Output BagMovement DTO
    """
    creation_datetime: datetime
    bag: BagDetailsDTO
    amount: float
