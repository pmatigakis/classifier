from os import path

from classifier.ml import Classifier


TESTING = True
DEBUG = False

SECRET_KEY = "testing_secret_key"

SQLALCHEMY_DATABASE_URI = "sqlite://"

ENABLE_LOGGING = False

classifiers_path = path.join(
    path.dirname(path.abspath(__file__)), "..", "classifiers")

CLASSIFIERS = {
    "iris": Classifier(
        classifier=path.join(classifiers_path, "iris", "classifier.pickle")
    ),
    "iris_probabilities": Classifier(
        classifier=path.join(classifiers_path, "iris", "classifier.pickle"),
        probabilities=True
    ),
    "iris_with_data_extractor": Classifier(
        data_extractor=lambda r: r[0:4],
        classifier=path.join(classifiers_path, "iris", "classifier.pickle")
    ),
    "iris_with_result_processor": Classifier(
        classifier=path.join(classifiers_path, "iris", "classifier.pickle"),
        result_processor=lambda r: {"data": r}
    ),
}

ERROR_404_HELP = False

HOST = "127.0.0.1"
PORT = 8022
