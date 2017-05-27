import logging
from logging.handlers import RotatingFileHandler

from flask import Flask
from flask_restful import Api
from raven.handlers.logging import SentryHandler

from classifier.resources import (ClassifierResource, ClassifiersResource,
                                  HealthResource, InformationResource)
from classifier import configuration


def initialize_logging(app):
    log_format = "%(asctime)s %(levelname)s [%(process)d:%(thread)d] " \
                 "%(name)s [%(pathname)s:%(funcName)s:%(lineno)d] %(message)s"
    formatter = logging.Formatter(log_format)

    logger = logging.getLogger("classifier")

    log_level = app.config["LOG_LEVEL"]

    if app.config["DEBUG"]:
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        stream_handler.setLevel(logging.DEBUG)
        logger.addHandler(stream_handler)
        log_level = logging.DEBUG

    handler = RotatingFileHandler(
        filename=app.config["LOG_FILE"],
        maxBytes=app.config["LOG_FILE_SIZE"],
        backupCount=app.config["LOG_FILE_COUNT"],
        encoding="utf8"
    )

    handler.setFormatter(formatter)
    handler.setLevel(log_level)
    logger.addHandler(handler)
    logger.setLevel(log_level)


def initialize_sentry(app):
    handler = SentryHandler(app.config["SENTRY_DSN"])
    handler.setLevel(app.config["SENTRY_LOG_LEVEL"])

    logger = logging.getLogger("classifier")
    logger.addHandler(handler)


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

    if app.config["SENTRY_DSN"]:
        initialize_sentry(app)

    api = Api(app)

    api.add_resource(
        ClassifierResource, "/api/v1/predict/<string:classifier>")

    api.add_resource(ClassifiersResource, "/api/v1/classifiers")
    api.add_resource(HealthResource, "/service/health")
    api.add_resource(InformationResource, "/service/information")

    return app
