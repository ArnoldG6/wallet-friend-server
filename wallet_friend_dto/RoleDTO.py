"""
@author: "Arnoldo J. González Quesada".
Github username: "ArnoldG6".
Contact me via "arnoldgq612@gmail.com".
GPL-3.0 license ©2022
"""
from typing import List

import pydantic
from pydantic import BaseModel

from wallet_friend_dto.PermissionDTO import PermissionDetailsDTO

"""
==========================Output DTOs.==========================
"""


@pydantic.dataclasses.dataclass(frozen=True)
class RoleDetailsDTO(BaseModel):
    """
    Output Role DTO
    """
    name: str
    description: str
    permissions: List[PermissionDetailsDTO]
