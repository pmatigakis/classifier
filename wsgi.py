import os

from classifier.application import create_app


settings_file = os.getenv("CLASSIFIER_SETTINGS")

if settings_file is None:
    print("The environment variable CLASSIFIER_SETTINGS is not set")
    exit(1)

app = create_app(settings_file)
