"""
@author: "Arnoldo J. González Quesada".
Github username: "ArnoldG6".
Contact me via "arnoldgq612@gmail.com".
GPL-3.0 license ©2022
"""


class WalletFriendException(BaseException):
    """
    Custom BaseException-child class for custom exceptions.
    """

    def __init__(self, message: str or None = ""):
        self.__message = message


class IncorrectParameterValueException(WalletFriendException):
    def __init__(self, message: str = None):
        """
        :param message: Custom user message.
        """
        if not message:
            super().__init__("Invalid parameter value")
        else:
            super().__init__(message)


class SingletonObjectException(WalletFriendException):
    def __init__(self):
        super().__init__("Singleton Object Exception.")


class ExistentEntityException(WalletFriendException):
    def __init__(self, message: str = None):
        """
        :param message: Custom user message.
        """
        if not message:
            super().__init__("Data already exists.")
        else:
            super().__init__(message)
