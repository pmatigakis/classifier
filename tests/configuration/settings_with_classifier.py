from os import path

from classifier.ml import MultiLabelClassifier


TESTING = True
DEBUG = False

SECRET_KEY = "testing_secret_key"

SQLALCHEMY_DATABASE_URI = "sqlite://"

ENABLE_LOGGING = False

classifiers_path = path.join(
    path.dirname(path.abspath(__file__)), "..", "classifiers")

CLASSIFIERS = {
    "labels": MultiLabelClassifier(
        binarizer=path.join(
            classifiers_path, "multilabel", "binarizer.pickle"),
        classifier=path.join(
            classifiers_path, "multilabel", "classifier.pickle")
    )
}
