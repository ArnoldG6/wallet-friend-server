"""
@author: "Arnoldo J. González Quesada".
Github username: "ArnoldG6".
Contact me via "arnoldgq612@gmail.com".
GPL-3.0 license ©2022
"""
import logging
from flask import request as f_request

from wallet_friend_exceptions.HttpWalletFriendExceptions import ExpiredRequestException, MalformedRequestException, \
    ExistentRecordException, HttpWalletFriendException
from wallet_friend_services import AuthService


class BagService:
    """
    The present class manages HTTP client requests that depends on
    Bag class objects information and operations.
    """

    def __init__(self, request: f_request):
        if request is None:
            raise ExpiredRequestException()
        self.__request = request


