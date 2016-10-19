from flask import Flask
from flask_restful import Api

from classifier.authentication import identity, authenticate, payload_handler
from classifier.resources import QueryResource
from classifier.extensions import jwt
from classifier.models import db


def create_app(settings_file):
    app = Flask(__name__)

    app.config.from_pyfile(settings_file)

    api = Api(app)

    api.add_resource(QueryResource, "/api/v1/query")

    db.init_app(app)

    jwt.identity_callback = identity
    jwt.authentication_callback = authenticate
    jwt.jwt_payload_callback = payload_handler
    jwt.init_app(app)

    return app
