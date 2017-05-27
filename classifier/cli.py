from os import path, getcwd, getenv
import logging
import hashlib

from flask_script import Manager, Command
from flask import current_app
from consul import Consul, Check

from classifier.application import create_app
from classifier.servers import ClassifierServer


logger = logging.getLogger(__name__)


def generate_service_id(service_name, host, port):
    """Create the service id for consul
    :param str service_name: the service name
    :param str host: the service address
    :param int port: the port on which the service listens to
    :rtype: str
    :return: the service id
    """
    service_info = "{}-{}-{}".format(service_name, host, port).encode("utf-8")

    return "{}".format(hashlib.md5(service_info).hexdigest())


class RunServer(Command):
    def _register_service(self, configuration):
        logger.info("registering service to consul")

        client = Consul(
            host=configuration["CONSUL_HOST"],
            port=configuration["CONSUL_PORT"],
            scheme=configuration["CONSUL_SCHEME"],
            verify=configuration["CONSUL_VERIFY_SSL"]
        )

        health_address = "http://{host}:{port}/service/health"

        health_http = Check.http(
            url=health_address.format(
                host=configuration["HOST"],
                port=configuration["PORT"]
            ),
            interval=configuration["CONSUL_HEALTH_INTERVAL"],
            timeout=configuration["CONSUL_HEALTH_TIMEOUT"]
        )

        client.agent.service.register(
            name=configuration["SERVICE_NAME"],
            service_id=generate_service_id(
                configuration["SERVICE_NAME"],
                configuration["HOST"],
                configuration["PORT"]
            ),
            address=configuration["HOST"],
            port=configuration["PORT"],
            check=health_http
        )

    def _on_starting(self, server):
        logger.info("server started")

        if server.app.application.config.get("CONSUL_HOST") is not None:
            self._register_service(server.app.application.config)

    def _on_exit(self, server):
        logger.info("server stopped")

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
            "workers": 4,
            "max_requests": worker_max_requests,
            "max_requests_jitter": worker_request_jitter,
            # we have to setup the hooks using lambdas in order to avoid the
            # function arity checks of gunicorn
            "on_starting": lambda server: self._on_starting(server),
            "on_exit": lambda server: self._on_exit(server)
        }

        ClassifierServer(current_app, options).run()


def main():
    settings_file = path.join(getcwd(), "settings.py")

    environment_type = getenv("CLASSIFIER_ENV_TYPE", "production")

    app = create_app(settings_file, environment_type)

    manager = Manager(app)
    manager.add_command("runserver", RunServer)

    manager.run()
