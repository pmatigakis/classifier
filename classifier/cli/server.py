import logging

from classifier.servers import ClassifierServer
from classifier.wsgi import app


logger = logging.getLogger(__name__)


def main():
    logger.info("starting classifier server")

    server = ClassifierServer(app)
    server.run()
