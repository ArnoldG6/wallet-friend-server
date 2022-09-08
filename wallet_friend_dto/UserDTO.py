"""
@author: "Arnoldo J. González Quesada".
Github username: "ArnoldG6".
Contact me via "arnoldgq612@gmail.com".
GPL-3.0 license ©2022
"""
from datetime import datetime
from typing import List

import pydantic
from pydantic import BaseModel, validator

from wallet_friend_entities import Role
from wallet_friend_tools import check_non_empty_non_spaces_string

"""
=============================================User-related DTOs.=============================================
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
        raise ValueError('username must not be blank or contain illegal characters.')

    @validator("password")
    def validate_pwd(cls, v):
        if check_non_empty_non_spaces_string(v):
            return v
        raise ValueError('password must not be blank or contain illegal characters.')


@pydantic.dataclasses.dataclass(frozen=True)
class UserDetailsDTO(BaseModel):
    """
    Output DTO for displaying user information.
    """
    username: str
    email: str
    first_name: str
    last_name: str  # Last name does not require validation.
    enabled: bool
    creation_datetime: datetime
    roles: List[Role] = []

    @validator("username")
    def validate_username(cls, v):
        if check_non_empty_non_spaces_string(v):
            return v
        raise ValueError('username must not be blank or contain illegal characters.')

    @validator("email")
    def validate_email(cls, v):
        if check_non_empty_non_spaces_string(v):
            return v
        raise ValueError('email must not be blank or contain illegal characters.')

    @validator("first_name")
    def validate_first_name(cls, v):
        if check_non_empty_non_spaces_string(v):
            return v
        raise ValueError('first_name must not be blank or contain illegal characters.')
    """
    @validator("roles")
    def validate_roles(cls, v):
        if v:  # Not empty list.
            return v
        raise ValueError("User's roles cannot be empty.")
    """