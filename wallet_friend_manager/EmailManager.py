"""
@author: "Miguel González Carvajal".
Github username: "Miguelgonz98".
Contact me via "mgonzalex236@gmail.com".
GPL-3.0 license ©2022
"""
import datetime
import os
import smtplib
import logging

from wallet_friend_exceptions.WalletFriendExceptions import SingletonObjectException
from wallet_friend_entities.Entities import User

EMAIL_ADDRESS = 'walletfriendofficial@outlook.com'
EMAIL_PASSWORD = '!QAZ2wsx#EDC'


class EmailManager:
    __email_manager_singleton = None  # Singleton EmailManager object

    def __init__(self):
        if EmailManager.__email_manager_singleton is not None:
            raise SingletonObjectException()
        else:
            EmailManager.__email_manager_singleton = self

    @staticmethod
    def get_instance():
        """
        Returns:
            EmailManager: the EmailManager class singleton object.
        """
        if EmailManager.__email_manager_singleton is None:
            EmailManager.__email_manager_singleton = EmailManager()
        return EmailManager.__email_manager_singleton

    def send_reset_password(self, user: User, code: str):
        try:
            subject = 'Wallet Friend User Reset Password'
            body = f'Hello {user.first_name} {user.last_name}, this is an email from Wallet Friend Support account to reset your password. You must access the following link: {code}'
            message = 'Subject: {}\n\n{}'.format(subject, body)
            server = smtplib.SMTP('smtp-mail.outlook.com', 587)
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, user.email, message.encode("utf8"))
            server.quit()
        except BaseException as e:  # Any Exception
            logging.exception(f"Email Creation Failed. Details: {e}")
            raise e

    def send_change_password(self, user: User):
        try:
            subject = 'Wallet Friend Changed User Password'
            body = f'Hello {user.first_name} {user.last_name}, this is an email from Wallet Friend Support account to notify a change of password. ' \
                      f'Password has been changed on {(datetime.now()).strftime("%d/%m/%Y, %H:%M:%S")}'
            message = 'Subject: {}\n\n{}'.format(subject, body)
            server = smtplib.SMTP('smtp-mail.outlook.com', 587)
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, user.email, message.encode("utf8"))
            server.quit()
        except Exception as e:  # Any Exception
            logging.exception(f"Email Creation Failed. Details: {e}")
            raise e
