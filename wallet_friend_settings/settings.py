"""
@author: "Arnoldo J. González Quesada".
Github username: "ArnoldG6".
Contact me via "arnoldgq612@gmail.com".
GPL-3.0 license ©2022
"""


def default_password_pattern():
    """
    :return: regex with the string that all system passwords must match.
    """
    return "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[$&+,:;=?@#|'<>.^*()%!-,]).{8,}$"


def default_email_pattern():
    """
    :return: regex with the string that all system emails must match.
    """
    return r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'


def default_db_settings_path():
    """
    :return: str that contains db settings file for DAO's use.
    """
    return "wallet_friend_db/config.ini"
