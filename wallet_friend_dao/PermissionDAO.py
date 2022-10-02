"""
@author: "Arnoldo J. González Quesada".
Github username: "ArnoldG6".
Contact me via "arnoldgq612@gmail.com".
GPL-3.0 license ©2022
"""
from enum import Enum


class ClientPermission(Enum):
    """
    Class to define default-permission info for client
    It is associated with all client-related roles.
    """
    NAME = "Set account balance"
    DESCRIPTION = "User can add or withdraw money-representation from account"
