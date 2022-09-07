"""
@author: "Arnoldo J. González Quesada".
Github username: "ArnoldG6".
Contact me via "arnoldgq612@gmail.com".
GPL-3.0 license ©2022
"""

from flask import request as f_request


class AuthService:
    """
    The present class manages HTTP client requests that depends on
    User class objects information and operations.
    """

    def __init__(self, request: f_request):
        if request is None:
            raise Exception("Expired request exception")
        self.__request = request


