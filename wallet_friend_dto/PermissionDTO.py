"""
@author: "Arnoldo J. González Quesada".
Github username: "ArnoldG6".
Contact me via "arnoldgq612@gmail.com".
GPL-3.0 license ©2022
"""

import pydantic
from pydantic import BaseModel

"""
==========================Output DTOs.==========================
"""


@pydantic.dataclasses.dataclass(frozen=True)
class PermissionDetailsDTO(BaseModel):
    """
    Output Permission DTO
    """
    name: str
    description: str
