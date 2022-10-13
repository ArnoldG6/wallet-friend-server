"""
@author: "Arnoldo J. González Quesada".
Github username: "ArnoldG6".
Contact me via "arnoldgq612@gmail.com".
GPL-3.0 license ©2022
"""


def check_non_empty_non_spaces_string(s: str) -> bool:
    """
    param s: str to be checked
    :return: True or False depending on string's validity.
    """
    if not s or not s.replace(" ", "") or " " in s:
        return False
    return True


def check_non_empty_string(s: str) -> bool:
    """
    param s: str to be checked
    :return: True if str is empty, False if not.
    """
    if not s or len(s.replace(" ", "")) == 0:
        return False
    return True


