"""
@author: "Arnoldo J. González Quesada".
Github username: "ArnoldG6".
Contact me via "arnoldgq612@gmail.com".
GPL-3.0 license ©2022
"""
import re
from datetime import datetime
from typing import List

import pydantic
from pydantic import BaseModel, validator

from wallet_friend_dto.RoleDTO import RoleDetailsDTO
from wallet_friend_exceptions.HttpWalletFriendExceptions import MalformedRequestException
from wallet_friend_settings import default_password_pattern
from wallet_friend_settings.settings import default_email_pattern
from wallet_friend_tools import check_non_empty_non_spaces_string

"""
=============================================User-related DTOs.=============================================
"""

"""
==========================Input DTOs.==========================
"""


class UserAuthDTO(BaseModel):
    """
    Input DTO for user authentication.
    """
    username: str  # Username or email.
    password: str  # Sha-256 hashed password.

    @validator("username")
    def validate_username(cls, v):
        if check_non_empty_non_spaces_string(v):
            return v
        raise MalformedRequestException("Invalid value for parameter 'username'")

    @validator("password")
    def validate_pwd(cls, v):
        if re.fullmatch(default_password_pattern(), v):
            return v
        raise MalformedRequestException("Invalid value for parameter 'password'")


class UserRegisterDTO(BaseModel):
    """
    Input DTO for user registration.
    """

    username: str  # Username or email.
    password: str  # NOT Sha-256 hashed password.
    email: str
    first_name: str
    last_name: str

    @validator("email")
    def validate_email(cls, v):
        # Email pattern regex.
        if check_non_empty_non_spaces_string(v) and re.fullmatch(default_email_pattern(), v):
            return v
        raise MalformedRequestException("Invalid value for parameter 'email'")

    @validator("password")
    def validate_password(cls, v):
        # Email pattern regex.
        if re.fullmatch(default_password_pattern(), v):
            return v
        raise MalformedRequestException("Invalid value for parameter 'password'")


"""
==========================Output DTOs.==========================
"""


@pydantic.dataclasses.dataclass(frozen=True)
class UserDetailsDTO(BaseModel):
    """
    Output DTO for displaying user information.
    """


@pydantic.dataclasses.dataclass(frozen=True)
class UserDetailsDTO(BaseModel):
    """
    Output DTO for displaying user information.
    """
    username: str
    email: str
    first_name: str
    last_name: str  # Last name does not require validation because not everyone got a last name.
    enabled: bool
    creation_datetime: datetime
    roles: list

    @validator("username")
    def validate_username(cls, v):
        if check_non_empty_non_spaces_string(v):
            return v
        raise MalformedRequestException("Invalid value for parameter 'username'")

    @validator("email")
    def validate_email(cls, v):
        # Email pattern regex.
        if check_non_empty_non_spaces_string(v) and re.fullmatch(default_email_pattern(), v):
            return v
        raise MalformedRequestException("Invalid value for parameter 'email'")

    @validator("first_name")
    def validate_first_name(cls, v):
        if check_non_empty_non_spaces_string(v):
            return v
        raise MalformedRequestException("Invalid value for parameter 'first_name'")
