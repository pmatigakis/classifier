from os import path, getcwd, getenv
import logging

from flask_script import Manager, Command
from flask import current_app

from classifier.application import create_app
from classifier.servers import ClassifierServer


logger = logging.getLogger(__name__)


class RunServer(Command):
    def run(self):
        server = ClassifierServer(current_app)

        server.run()


def main():
    settings_file = path.join(getcwd(), "settings.py")

    environment_type = getenv("CLASSIFIER_ENV_TYPE", "production")

    app = create_app(settings_file, environment_type)

    manager = Manager(app)
    manager.add_command("runserver", RunServer)

    manager.run()
