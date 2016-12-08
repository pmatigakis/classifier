from classifier.ml import Classifier


SECRET_KEY = "dfgdfgfdgfsdgdfretre563tgteh4675434t"

DEBUG = True

SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://postgres:postgres@localhost:5432/classifier"

PROPAGATE_EXCEPTIONS = True

ENABLE_LOGGING = False

CLASSIFIERS = {
    "classify": Classifier(
        classifier="classifier.pickle"
    )
}
