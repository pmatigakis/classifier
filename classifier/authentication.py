import logging

from flask_jwt import _default_jwt_payload_handler

from models import User


logger = logging.getLogger(__name__)


def authenticate(username, password):
    logger.info("authenticating using jwt: user(%s)", username)

    return User.authenticate(username, password)


def identity(payload):
    user_id = payload["identity"]
    jti = payload["jti"]

    msg = "authenticating using jwt: user_id(%d) jwt(%s)"
    logger.info(msg, user_id, jti)

    return User.authenticate_using_jti(user_id, jti)


def payload_handler(user):
    payload = _default_jwt_payload_handler(user)
    payload["jti"] = user.jti
    return payload
