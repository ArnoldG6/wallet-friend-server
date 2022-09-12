"""
@author: "Arnoldo J. González Quesada".
Github username: "ArnoldG6".
Contact me via "arnoldgq612@gmail.com".
GPL-3.0 license ©2022
"""
import json as json

from wallet_friend_exceptions.WalletFriendExceptions import WalletFriendException


class HttpWalletFriendException(WalletFriendException):
    """
    Custom base Exception class for HTTP error responses.
    """

    def __init__(self, message: str or None = "", error_code: int or None = None):
        self.__message = message
        self.__error_code = error_code

    def json(self):
        return json.dumps({
            "code": self.__error_code,
            "message": self.__message
        })

    def get_code(self):
        return self.__error_code

    def get_description(self):
        return self.__message


class MalformedRequestException(HttpWalletFriendException):
    def __init__(self, message: str = None):
        """
        :param message: Custom user message.
        """
        if not message:
            super().__init__("Incorrect content sent in request-JSON body.", 400)
        else:
            super().__init__(message, 400)


class ExistentEntityException(HttpWalletFriendException):
    def __init__(self, message: str = None):
        """
        :param message: Custom user message.
        """
        if not message:
            super().__init__("Data already exists.", 400)
        else:
            super().__init__(message, 400)


class NotAuthorizedException(HttpWalletFriendException):
    def __init__(self):
        super().__init__("Authentication failure.", 401)


class DisabledUserException(HttpWalletFriendException):
    def __init__(self):
        super().__init__("User is disabled. Contact your administrator.", 401)


class ForbiddenException(HttpWalletFriendException):
    def __init__(self):
        super().__init__("Not permitted to access.", 403)


class NotFoundException(HttpWalletFriendException):
    def __init__(self):
        super().__init__("Resource not found.", 404)


class ExpiredRequestException(HttpWalletFriendException):
    def __init__(self):
        super().__init__("Request has expired.", 410)


class InternalServerException(HttpWalletFriendException):
    def __init__(self):
        super().__init__("Internal Server Error.", 500)


class ServiceUnavailableException(HttpWalletFriendException):
    def __init__(self):
        super().__init__("Server is temporarily unavailable or busy.", 503)


"""
https://dennis-xlc.gitbooks.io/restful-java-with-jax-rs-2-0-2rd-edition/content/en/part1/chapter7/exception_handling.html
BadRequestException	400	Malformed message
NotAuthorizedException	401	Authentication failure
ForbiddenException	403	Not permitted to access
NotFoundException	404	Could not find resource
NotAllowedException	405	HTTP method not supported
NotAcceptableException	406	Client media type requested not supported
NotSupportedException	415	Client posted media type not supported
InternalServerErrorException	500	General server error
ServiceUnavailableException	503	Server is temporarily unavailable or busy
https://www.restapitutorial.com/httpstatuscodes.html
"""
