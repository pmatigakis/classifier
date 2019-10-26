from os import path

from classifier.ml import Classifier


TESTING = True
DEBUG = False

SECRET_KEY = "testing_secret_key"

SQLALCHEMY_DATABASE_URI = "sqlite://"

classifiers_path = path.join(
    path.dirname(path.abspath(__file__)), "..", "classifiers")

CLASSIFIERS = {
    "iris": Classifier(
        classifier=path.join(classifiers_path, "iris", "classifier.joblib")
    ),
    "iris_probabilities": Classifier(
        classifier=path.join(classifiers_path, "iris", "classifier.joblib"),
        probabilities=True
    )
}

ERROR_404_HELP = False

HOST = "127.0.0.1"
PORT = 8022
