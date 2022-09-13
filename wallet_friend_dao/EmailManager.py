"""
@author: "Miguel González Carvajal".
Github username: "Miguelgonz98".
Contact me via "mgonzalex236@gmail.com".
GPL-3.0 license ©2022
"""
import os
import smtplib

from wallet_friend_exceptions.WalletFriendExceptions import SingletonObjectException

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

    def send_reset_password(self, user, code):
        subject = 'Wallet Friend User Reset Password'
        message = 'Hello {fName} {lName}, this is a email from Wallet Friend Support account to reset your password. ' \
                  'You must access the following link: {uCode}'.format(fName=user.first_name,
                                                                       lName=user.last_name,
                                                                       uCode=code)
        message = 'Subject: {}\n\n{}'.format(subject, message)
        server = smtplib.SMTP('smtp-mail.outlook.com', 587)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, user.email, message)
        server.quit()

    def send_change_password(self,user):
        pass


