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
    logger.handlers = []

    log_level = app.config["LOG_LEVEL"]

    if app.config["DEBUG"]:
        log_level = logging.DEBUG

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    stream_handler.setLevel(log_level)
    logger.addHandler(stream_handler)

    if app.config["LOG_FILE"] is not None:
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


def create_app(settings_file):
    app = Flask(__name__)

    app.config.from_object(configuration.Default)
    app.config.from_pyfile(settings_file)

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
