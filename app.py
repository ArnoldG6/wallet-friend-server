"""
@author: "Arnoldo J. González Quesada".
Github username: "ArnoldG6".
Contact me via "arnoldgq612@gmail.com".
GPL-3.0 license ©2022
"""
import logging
import secrets

from flask import Flask, request, make_response
from flask_cors import CORS

from wallet_friend_exceptions.HttpWalletFriendExceptions import InternalServerException, HttpWalletFriendException, \
    ServiceUnavailableException
from wallet_friend_services import AuthService

"""
HTTP server config.
"""
app = Flask(__name__)
CORS(app)  # Enabling CORS on whole app, if it is necessary, this should be changed for every path.
secret_key = secrets.token_urlsafe(256)  # setting secret  with newly generated secret SHA256 key.
app.secret_key = secret_key
api_versions = ["v1.0"]
latest_version = api_versions[-1]

"""
==============================================SO User web services==================================================
"""


@app.route(f"/{latest_version}/api/users/authenticate", methods=["POST"])
def users_authenticate():
    try:
        return AuthService(request).auth_user_service(secret_key), 200
    except HttpWalletFriendException as e:
        logging.error(e)
        return e.json(), e.get_code(),

    except BaseException as e:
        logging.error(e)
        e = InternalServerException()  # Exception overwrite to protect server's logs.
        return e.json(), e.get_code()


@app.route(f"/{latest_version}/api/users/register", methods=["POST"])
def users_register():
    try:
        return AuthService(request).register_user_service(), 200
    except HttpWalletFriendException as e:
        logging.error(e)
        return e.json(), e.get_code()

    except BaseException as e:
        logging.error(e)
        e = InternalServerException()  # Exception overwrite to protect server's logs.
        return e.json(), e.get_code()


"""
================================================EO User web services================================================
"""


def start_development_server():
    """
    Warning!: Development use only.  Do not use on production.
    """
    logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] %(asctime)s - %(message)s')
    app.run(threaded=True, port=80)


if __name__ == '__main__':
    start_development_server()
