"""
@author: "Miguel González Carvajal".
Github username: "Miguelgonz98".
Contact me via "mgonzalex236@gmail.com".
GPL-3.0 license ©2022
"""
import smtplib

message = 'Hello, this is a test email from Wallet Friend Support account'
subject = 'Wallet Friend Email Test'
message = 'Subject: {}\n\n{}'.format(subject,message)

server = smtplib.SMTP('smtp-mail.outlook.com',587)
server.starttls()
server.login('walletfriendofficial@outlook.com','!QAZ2wsx#EDC')
server.sendmail('walletfriendofficial@outlook.com',['mgonzalex236@gmail.com',
                                                    'arnoldgq612@gmail.com',
                                                    'ld.ramirezch14@gmail.com'],message)
server.quit()

print('Email was sent successfully!')

