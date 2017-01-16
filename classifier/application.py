import logging
from logging.handlers import RotatingFileHandler

from flask import Flask
from flask_restful import Api

from classifier.resources import ClassifierResource, ClassifiersResource


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


def create_app(settings_file):
    app = Flask(__name__)

    app.config.from_pyfile(settings_file)

    if app.config["ENABLE_LOGGING"]:
        initialize_logging(app)

    api = Api(app)

    api.add_resource(
        ClassifierResource, "/api/v1/predict/<string:classifier>")

    api.add_resource(ClassifiersResource, "/api/v1/classifiers")

    return app
