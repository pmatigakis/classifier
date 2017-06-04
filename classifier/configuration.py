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

    CONSUL_HOST = None
    CONSUL_PORT = 8500
    CONSUL_SCHEME = "http"
    CONSUL_VERIFY_SSL = True
    CONSUL_HEALTH_INTERVAL = "10s"
    CONSUL_HEALTH_TIMEOUT = "5s"
    SERVICE_NAME = "classifier"

    SENTRY_DSN = None
    SENTRY_LOG_LEVEL = logging.ERROR

    WORKER_MAX_REQUESTS = 100
    WORKER_MAX_REQUESTS_JITTER = 10
    WORKERS = 2


class Development(Default):
    SECRET_KEY = "development"
    DEBUG = True


class Testing(Default):
    SECRET_KEY = "testing"
    TESTING = True


class Production(Default):
    ENABLE_LOGGING = True
