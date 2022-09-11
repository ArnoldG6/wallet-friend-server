"""
@author: "Arnoldo J. González Quesada".
Github username: "ArnoldG6".
Contact me via "arnoldgq612@gmail.com".
GPL-3.0 license ©2022
"""
import logging
import secrets

from flask import Flask, request
from flask_cors import CORS
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


@app.route(f"/{latest_version}/users/auth", methods=["POST"])
def check_authorization():
    try:
        result = AuthService(request).auth_user_service(secret_key)
        return result, 200
    except Exception as e:
        logging.exception(e)
        return {"error_code": 500, "error_desc": "Internal Server Error"}, 500


def start_development_server():
    """
    Warning!: Development use only.  Do not use on production.
    """
    logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] %(asctime)s - %(message)s')
    app.run(threaded=True, port=80)


if __name__ == '__main__':
    start_development_server()
