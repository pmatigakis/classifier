from classifier.ml import Classifier


SECRET_KEY = "dfgdfgfdgfsdgdfretre563tgteh4675434t"

DEBUG = True

PROPAGATE_EXCEPTIONS = True

HOST = "192.168.1.101"
PORT = 8022

CLASSIFIERS = {
    "iris": Classifier(
        classifier="classifier.pickle"
    )
}


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
        }
    },
    "root": {
        'level': 'INFO',
    }
}
