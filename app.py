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

from wallet_friend_exceptions.HttpWalletFriendExceptions import InternalServerException, HttpWalletFriendException
from wallet_friend_services import AuthService, MovementService, FixedMovementService
from wallet_friend_services.BagServices import BagService

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


@app.route(f"/api/{latest_version}/users/authenticate", methods=["POST"])
def users_authenticate():
    try:
        return AuthService(request).auth_user_service(secret_key), 200
    except HttpWalletFriendException as e:
        logging.exception(e)
        return e.json(), e.get_code(),

    except BaseException as e:
        logging.exception(e)
        e = InternalServerException()  # Exception overwrite to protect server's logs.
        return e.json(), e.get_code()


@app.route(f"/api/{latest_version}/users/register", methods=["POST"])
def users_register():
    try:
        AuthService(request).register_user_service()
        return {"success": True}, 200
    except HttpWalletFriendException as e:
        logging.exception(e)
        return e.json(), e.get_code()

    except BaseException as e:
        logging.exception(e)
        e = InternalServerException()  # Exception overwrite to protect server's logs.
        return e.json(), e.get_code()


@app.route(f"/api/{latest_version}/users/check-authorization/<username>", methods=["GET"])
def users_check_authorization(username):
    try:
        return AuthService(request).check_authorization_user_service(username), 200
    except HttpWalletFriendException as e:
        logging.exception(e)
        return e.json(), e.get_code()

    except BaseException as e:
        logging.exception(e)
        e = InternalServerException()  # Exception overwrite to protect server's logs.
        return e.json(), e.get_code()


@app.route(f"/api/{latest_version}/users/reset_password", methods=["POST"])
def users_reset_password():
    try:
        AuthService(request).reset_password_service(latest_version)
        return {"success": True}, 201
    except HttpWalletFriendException as e:
        logging.exception(e)
        return e.json(), e.get_code()
    except BaseException as e:
        logging.exception(e)
        e = InternalServerException()  # Exception overwrite to protect server's logs.
        return e.json(), e.get_code()


"""
================================================EO User web services================================================
"""

"""
==============================================SO Movement web services==================================================
"""


@app.route(f"/api/{latest_version}/movements/single", methods=["POST"])
def movements_create_single_movement():
    try:
        MovementService(request).create_single_movement_service()
        return {"success": True}, 201
    except HttpWalletFriendException as e:
        logging.exception(e)
        return e.json(), e.get_code()
    except BaseException as e:
        logging.exception(e)
        e = InternalServerException()  # Exception overwrite to protect server's logs.
        return e.json(), e.get_code()


@app.route(f"/api/{latest_version}/movements/fixed", methods=["POST"])
def movements_create_fixed_movement():
    try:
        FixedMovementService(request).create_fixed_movement_service()
        return {"success": True}, 201
    except HttpWalletFriendException as e:
        logging.exception(e)
        return e.json(), e.get_code()
    except BaseException as e:
        logging.exception(e)
        e = InternalServerException()  # Exception overwrite to protect server's logs.
        return e.json(), e.get_code()


@app.route(f"/api/{latest_version}/movements/<movement_id>", methods=["DELETE"])
def movements_delete_movement(movement_id):
    try:
        MovementService(request).delete_movement_service(movement_id)
        return {"success": True}, 201
    except HttpWalletFriendException as e:
        logging.exception(e)
        return e.json(), e.get_code()
    except BaseException as e:
        logging.exception(e)
        e = InternalServerException()  # Exception overwrite to protect server's logs.
        return e.json(), e.get_code()


@app.route(f"/api/{latest_version}/movements/assign-to-bag", methods=["PATCH"])
def movements_assign_movement_to_bag():
    try:
        MovementService(request).add_bag_movement_to_movement_service()
        return {"success": True}, 201
    except HttpWalletFriendException as e:
        logging.exception(e)
        return e.json(), e.get_code()
    except BaseException as e:
        logging.exception(e)
        e = InternalServerException()  # Exception overwrite to protect server's logs.
        return e.json(), e.get_code()


"""
==============================================EO Movement web services==================================================
"""

"""
==============================================SO Bag web services==================================================
"""


@app.route(f"/api/{latest_version}/bags/create", methods=["POST"])
def create_bag():
    try:
        BagService(request).add_bag_service()
        return {"success": True}, 201
    except HttpWalletFriendException as e:
        logging.exception(e)
        return e.json(), e.get_code()
    except BaseException as e:
        logging.exception(e)
        e = InternalServerException()  # Exception overwrite to protect server's logs.
        return e.json(), e.get_code()


@app.route(f"/api/{latest_version}/bags/delete/<bag_id>", methods=["DELETE"])
def delete_bag(bag_id):
    try:
        BagService(request).delete_bag_service(bag_id)
        return {"success": True}, 201
    except HttpWalletFriendException as e:
        logging.exception(e)
        return e.json(), e.get_code()
    except BaseException as e:
        logging.exception(e)
        e = InternalServerException()  # Exception overwrite to protect server's logs.
        return e.json(), e.get_code()


@app.route(f"/api/{latest_version}/bags/bag_movements/delete/<bag_movement_id>", methods=["DELETE"])
def delete_bag_movement_from_bag(bag_movement_id):
    try:
        BagService(request).delete_bag_movement_from_bag_service(bag_movement_id)
        return {"success": True}, 201
    except HttpWalletFriendException as e:
        logging.exception(e)
        return e.json(), e.get_code()
    except BaseException as e:
        logging.exception(e)
        e = InternalServerException()  # Exception overwrite to protect server's logs.
        return e.json(), e.get_code()


@app.route("/testxd", methods=["GET"])
def test_route():
    return {"test_status": "okay"}, 200


"""
==============================================EO Bag web services==================================================
"""


if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] %(asctime)s - %(message)s')
   # app.run(threaded=True, port=80)
    app.run(threaded=True, port=5000)

