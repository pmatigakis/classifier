from flask_jwt import _default_jwt_payload_handler

from models import User


def authenticate(username, password):
    return User.authenticate(username, password)


def identity(payload):
    user_id = payload["identity"]
    jti = payload["jti"]
    return User.authenticate_using_jti(user_id, jti)


def payload_handler(user):
    payload = _default_jwt_payload_handler(user)
    payload["jti"] = user.jti
    return payload
