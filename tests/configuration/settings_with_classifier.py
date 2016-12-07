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
    "multilabel_with_binarizer": Classifier(
        binarizer=path.join(
            classifiers_path, "multilabel", "binarizer.pickle"),
        classifier=path.join(
            classifiers_path, "multilabel", "classifier.pickle"),
        probabilities=True
    ),
    "multilabel": Classifier(
        classifier=path.join(
            classifiers_path, "multilabel", "classifier.pickle"),
        probabilities=True
    ),
    "iris": Classifier(
        classifier=path.join(classifiers_path, "iris", "classifier.pickle")
    ),
    "iris_multilabel_with_binarizer": Classifier(
        binarizer=path.join(
            classifiers_path, "iris", "binarizer.pickle"),
        classifier=path.join(
            classifiers_path, "iris", "multilabel_classifier.pickle")
    ),
    "iris_with_data_extractor": Classifier(
        data_extractor=lambda r: r,
        classifier=path.join(classifiers_path, "iris", "classifier.pickle")
    ),
    "iris_with_result_processor": Classifier(
        classifier=path.join(classifiers_path, "iris", "classifier.pickle"),
        result_processor=lambda r: {"data": r}
    ),
}
