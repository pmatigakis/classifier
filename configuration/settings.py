import os
import re

from classifiers.classifiers import CategoryClassifier

from classifier.ml import Classifier

DEBUG = False

PROPAGATE_EXCEPTIONS = True

CLASSIFIERS = {
    "categories": Classifier(
        classifier=CategoryClassifier(),
        probabilities=True
    )
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
PORT = os.getenv("PORT", 8022)

WORKER_MAX_REQUESTS = int(os.getenv("WORKER_MAX_REQUESTS", 500))
WORKER_MAX_REQUESTS_JITTER = int(os.getenv("WORKER_MAX_REQUESTS_JITTER", 30))
WORKERS = int(os.getenv("WORKERS", 4))

CONSUL_HOST = os.getenv("CONSUL_HOST")
CONSUL_PORT = os.getenv("CONSUL_PORT", 8500)
CONSUL_SCHEME = "http"
CONSUL_VERIFY_SSL = True
CONSUL_HEALTH_INTERVAL = "10s"
CONSUL_HEALTH_TIMEOUT = "5s"

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': "%(asctime)s %(levelname)s [%(process)d:%(thread)d] %(name)s [%(pathname)s:%(funcName)s:%(lineno)d] %(message)s"
        }
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'classifier': {
            'handlers': ['console'],
            'propagate': True
        },
        'classifiers': {
            'handlers': ['console'],
            'propagate': True
        }
    },
    "root": {
        'level': 'INFO',
    }
}
