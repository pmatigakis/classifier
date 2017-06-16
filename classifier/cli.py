from os import path, getcwd
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

    app = create_app(settings_file)

    manager = Manager(app)
    manager.add_command("runserver", RunServer)

    manager.run()
