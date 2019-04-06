from distutils.util import strtobool
import os
import re

from classifiers.documents.categories.classifier import CategoryClassifier
from classifiers.keyword_selection.classifier import KeywordSelectionClassifier

from classifier.ml import Classifier

DEBUG = strtobool(os.getenv("DEBUG", "False"))
TESTING = strtobool(os.getenv("TESTING", "False"))

PROPAGATE_EXCEPTIONS = True

CLASSIFIERS = {
    "categories": Classifier(
        classifier=CategoryClassifier(),
        probabilities=True
    ),
    "select-keywords": Classifier(classifier=KeywordSelectionClassifier())
}


host_pattern = re.compile(r"^(.+?)\s+{}$".format(os.getenv("HOSTNAME")))
host = None
with open("/etc/hosts", "r") as f:
    for line in f:
        m = host_pattern.match(line)
        if m:
            host = m.group(1)
            break

if host is None:
    raise RuntimeError("failed to find the container ip address")

HOST = host
PORT = int(os.getenv("PORT", 8022))

WORKER_MAX_REQUESTS = int(os.getenv("WORKER_MAX_REQUESTS", 500))
WORKER_MAX_REQUESTS_JITTER = int(os.getenv("WORKER_MAX_REQUESTS_JITTER", 30))
WORKERS = int(os.getenv("WORKERS", 4))

CONSUL_HOST = os.getenv("CONSUL_HOST")
CONSUL_PORT = int(os.getenv("CONSUL_PORT", 8500))
CONSUL_SCHEME = os.getenv("CONSUL_SCHEME", "http")
CONSUL_VERIFY_SSL = strtobool(os.getenv("CONSUL_VERIFY_SSL", "True"))
CONSUL_HEALTH_INTERVAL = "10s"
CONSUL_HEALTH_TIMEOUT = "5s"

__handlers = {
    'console': {
        'level': os.getenv("CONSOLE_LOG_LEVEL", "INFO"),
        'class': 'logging.StreamHandler',
        'formatter': 'verbose'
    }
}

__sentry_dsn = os.getenv("SENTRY_DSN")
if __sentry_dsn:
    __handlers["sentry"] = {
        'level': os.getenv("SENTRY_LOG_LEVEL", "ERROR"),
        'class': 'raven.handlers.logging.SentryHandler',
        'dsn': __sentry_dsn
    }

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': "%(asctime)s %(levelname)s [%(process)d:%(thread)d] %(name)s [%(pathname)s:%(funcName)s:%(lineno)d] %(message)s"
        }
    },
    'handlers': __handlers,
    'loggers': {
        'classifier': {
            'handlers': __handlers.keys(),
            'propagate': True
        },
        'classifiers': {
            'handlers': __handlers.keys(),
            'propagate': True
        }
    },
    "root": {
        'level': os.getenv("ROOT_LOGGER_LEVEL", "INFO"),
    }
}
