import logging

from gunicorn.app.base import BaseApplication
from consul import Consul, Check

from classifier.service import generate_service_id


logger = logging.getLogger(__name__)


class ClassifierServer(BaseApplication):
    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super(ClassifierServer, self).__init__()

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

    def _deregister_service(self, configuration):
        logger.info("deregistering service from consul")

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
        logger.info("server started")

        if server.app.application.config.get("CONSUL_HOST") is not None:
            self._register_service(server.app.application.config)

    def _on_exit(self, server):
        logger.info("server stopped")

        if server.app.application.config.get("CONSUL_HOST") is not None:
            self._deregister_service(server.app.application.config)

    def load_config(self):
        for key, value in self.options.items():
            if key in self.cfg.settings and value is not None:
                self.cfg.set(key, value)

        # we have to setup the hooks using lambdas in order to avoid the
        # function arity checks of gunicorn
        self.cfg.set("on_starting", lambda server: self._on_starting(server))
        self.cfg.set("on_exit", lambda server: self._on_exit(server))

    def load(self):
        return self.application
