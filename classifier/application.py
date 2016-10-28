from os import path

from flask import Flask
from flask_restful import Api
from sklearn.externals import joblib

from classifier.authentication import identity, authenticate, payload_handler
from classifier.resources import QueryResource
from classifier.extensions import jwt, clf
from classifier.models import db
from classifier.ml import MultiLabelDocumentClassifier


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

    clf.init__app(app)

    data_path = app.config["DATA_PATH"]

    class_ids = joblib.load(path.join(data_path, "class_ids.pickle"))
    class_ids = {class_id: klass for klass, class_id in class_ids.items()}

    feature_extractor = joblib.load(
        path.join(data_path, "feature_extractor.pickle"))

    classifier = joblib.load(path.join(data_path, "classifier.pickle"))

    label_classifier = MultiLabelDocumentClassifier(
        class_ids, feature_extractor, classifier)

    clf.add_classifier("labels", label_classifier)

    return app
