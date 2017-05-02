from os import path, getcwd, getenv

from flask_script import Manager

from classifier.application import create_app


def main():
    settings_file = path.join(getcwd(), "settings.py")

    environment_type = getenv("CLASSIFIER_ENV_TYPE", "production")

    app = create_app(settings_file, environment_type)

    manager = Manager(app)

    manager.run()
