import logging.config

from flask import Flask
from flask_restful import Api

from classifier.resources import (ClassifierResource, ClassifiersResource,
                                  HealthResource, InformationResource)
from classifier import configuration


def initialize_logging(app):
    log_config = app.config.get("LOGGING")

    if log_config is not None:
        logging.config.dictConfig(log_config)


def create_app(settings_file):
    app = Flask(__name__)

    app.config.from_object(configuration.Default)
    app.config.from_pyfile(settings_file)

    initialize_logging(app)

    api = Api(app)

    api.add_resource(
        ClassifierResource, "/api/v1/predict/<string:classifier>")

    api.add_resource(ClassifiersResource, "/api/v1/classifiers")
    api.add_resource(HealthResource, "/service/health")
    api.add_resource(InformationResource, "/service/information")

    return app
