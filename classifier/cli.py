from os import path, getcwd, getenv
import logging

from flask_script import Manager, Command
from flask import current_app

from classifier.application import create_app
from classifier.servers import ClassifierServer


logger = logging.getLogger(__name__)


class RunServer(Command):
    def run(self):
        worker_max_requests = current_app.config.get(
            "WORKER_MAX_REQUESTS", 100)
        worker_request_jitter = current_app.config.get(
            "WORKER_MAX_REQUESTS_JITTER", 10)

        options = {
            "preload_app": False,
            "bind": "{host}:{port}".format(
                host=current_app.config["HOST"],
                port=current_app.config["PORT"]
            ),
            "workers": 1,
            "max_requests": worker_max_requests,
            "max_requests_jitter": worker_request_jitter
        }

        ClassifierServer(current_app, options).run()


def main():
    settings_file = path.join(getcwd(), "settings.py")

    environment_type = getenv("CLASSIFIER_ENV_TYPE", "production")

    app = create_app(settings_file, environment_type)

    manager = Manager(app)
    manager.add_command("runserver", RunServer)

    manager.run()
