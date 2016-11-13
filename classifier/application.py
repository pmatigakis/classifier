from os import path
import logging
from logging.handlers import RotatingFileHandler

from flask import Flask
from flask_restful import Api
from sklearn.externals import joblib

from classifier.authentication import identity, authenticate, payload_handler
from classifier.resources import MultiLabelClassifier
from classifier.extensions import jwt
from classifier.models import db
from classifier.ml import (extract_page_contents,
                           page_classification_result_processor)


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

    data_path = app.config["DATA_PATH"]

    class_ids = joblib.load(path.join(data_path, "class_ids.pickle"))
    class_ids = {class_id: klass for klass, class_id in class_ids.items()}

    feature_extractor = joblib.load(
        path.join(data_path, "feature_extractor.pickle"))

    feature_selector = joblib.load(
        path.join(data_path, "feature_selector.pickle"))

    classifier = joblib.load(path.join(data_path, "classifier.pickle"))

    api.add_resource(
        MultiLabelClassifier,
        "/api/v1/query",
        resource_class_kwargs={
            "data_extractor": extract_page_contents,
            "feature_extractor": feature_extractor,
            "feature_selector": feature_selector,
            "classifier": classifier,
            "labels": class_ids,
            "result_processor": page_classification_result_processor
        })

    db.init_app(app)

    jwt.identity_callback = identity
    jwt.authentication_callback = authenticate
    jwt.jwt_payload_callback = payload_handler
    jwt.init_app(app)

    return app
