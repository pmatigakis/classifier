import logging
from logging.handlers import RotatingFileHandler

from flask import Flask
from flask_restful import Api

from classifier.resources import ClassifierResource, ClassifiersResource
from classifier import configuration


def initialize_logging(app):
    log_level = app.config["LOG_LEVEL"]
    if app.config["DEBUG"]:
        log_level = logging.DEBUG

    handler = RotatingFileHandler(
        filename=app.config["LOG_FILE"],
        maxBytes=app.config["LOG_FILE_SIZE"],
        backupCount=app.config["LOG_FILE_COUNT"],
        encoding="utf8"
    )
    log_format = "%(asctime)s %(levelname)s [%(process)d:%(thread)d] " \
                 "%(name)s [%(pathname)s:%(funcName)s:%(lineno)d] %(message)s"
    formatter = logging.Formatter(log_format)

    handler.setFormatter(formatter)
    handler.setLevel(log_level)
    logger = logging.getLogger("classifier")
    logger.addHandler(handler)
    logger.setLevel(log_level)


def create_app(settings_file, environment_type=None):
    app = Flask(__name__)

    environment_type = environment_type or "production"

    environment_types = {
        "production": configuration.Production,
        "development": configuration.Development,
        "testing": configuration.Testing
    }

    app.config.from_object(environment_types[environment_type])

    app.config.from_pyfile(settings_file)

    if app.config["ENABLE_LOGGING"]:
        initialize_logging(app)

    api = Api(app)

    api.add_resource(
        ClassifierResource, "/api/v1/predict/<string:classifier>")

    api.add_resource(ClassifiersResource, "/api/v1/classifiers")

    return app
