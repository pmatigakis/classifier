import logging

from gunicorn.app.base import BaseApplication
from consul import Consul, Check

from classifier.service import generate_service_id


logger = logging.getLogger(__name__)


def _extract_gunicorn_options(configuration):
    options = {
        "preload_app": False,
        "bind": "{host}:{port}".format(
            host=configuration["HOST"],
            port=configuration["PORT"]
        ),
        "workers": configuration["WORKERS"],
        "worker_class": "sync",
        "max_requests": configuration["WORKER_MAX_REQUESTS"],
        "max_requests_jitter":
            configuration["WORKER_MAX_REQUESTS_JITTER"],
    }

    return options


class Server(BaseApplication):
    """A standalone gunicorn server"""

    def __init__(self, app, options=None):
        """Create a new Server object

        :param falcon.API app: the falcon application
        :param dict options: the gunicorn configuration
        """
        self.options = options or {}
        self.application = app

        super(Server, self).__init__()

    def load_config(self):
        for key, value in self.options.items():
            if key in self.cfg.settings and value is not None:
                self.cfg.set(key, value)

    def load(self):
        return self.application


class ClassifierServer(Server):
    """The classifier service server"""

    def __init__(self, app):
        """Create a new classifier service object

        :param Flask app: the Flask application
        """
        self.application = app
        options = _extract_gunicorn_options(app.config)

        super(ClassifierServer, self).__init__(app, options)

    def _register_service(self):
        """Register the service

        :param dict configuration: the application configuration
        """
        logger.info("registering service to consul")

        configuration = self.application.config

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

    def _deregister_service(self):
        """Deregister the service

        :param dict configuration: the application configuration
        """
        logger.info("deregistering service from consul")

        configuration = self.application.config

        client = Consul(
            host=configuration["CONSUL_HOST"],
            port=configuration["CONSUL_PORT"],
            scheme=configuration["CONSUL_SCHEME"],
            verify=configuration["CONSUL_VERIFY_SSL"]
        )

        service_id = generate_service_id(
            configuration["SERVICE_NAME"],
            configuration["HOST"],
            configuration["PORT"]
        )

        client.agent.service.deregister(
            service_id=service_id
        )

    def _on_starting(self, server):
        """Server is initializing

        :param server: the server object
        """
        logger.info("server started")

        if self.application.config.get("CONSUL_HOST") is not None:
            self._register_service()

    def _on_exit(self, server):
        """Server is shutting down

        :param server: the server object
        """
        logger.info("server stopped")

        if self.application.config.get("CONSUL_HOST") is not None:
            self._deregister_service()

    def load_config(self):
        super(ClassifierServer, self).load_config()

        # we have to setup the hooks using lambdas in order to avoid the
        # function arity checks of gunicorn
        self.cfg.set("on_starting", lambda server: self._on_starting(server))
        self.cfg.set("on_exit", lambda server: self._on_exit(server))
