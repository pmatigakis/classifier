import logging


class Default(object):
    SECRET_KEY = "secret-key"

    DEBUG = False
    TESTING = False

    PROPAGATE_EXCEPTIONS = True

    LOG_LEVEL = logging.INFO
    LOG_FILE_SIZE = 10000000
    LOG_FILE_COUNT = 5
    LOG_FILE = None

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
