import logging


class Default(object):
    DEBUG = False
    TESTING = False

    PROPAGATE_EXCEPTIONS = True

    ENABLE_LOGGING = False
    LOG_LEVEL = logging.INFO
    LOG_FILE_SIZE = 10000000
    LOG_FILE_COUNT = 5
    LOG_FILE = "classifier.log"


class Development(Default):
    SECRET_KEY = "development"
    DEBUG = True


class Testing(Default):
    SECRET_KEY = "testing"
    TESTING = True


class Production(Default):
    ENABLE_LOGGING = True
