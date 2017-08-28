import logging

from flask import current_app
from flask_restful import Resource, abort

import reqparsers

from classifier import __VERSION__

logger = logging.getLogger(__name__)


class ClassifierResource(Resource):
    def post(self, classifier):
        logger.info("running classifier: classifier={}".format(classifier))

        classifier_implementation = current_app.config["CLASSIFIERS"] \
                                               .get(classifier)

        if classifier_implementation is None:
            logger.warning(
                "unknown classifier: classifier={}".format(classifier))

            return abort(
                404,
                error="unknown classifier",
                classifier=classifier
            )

        args = reqparsers.classifier_data.parse_args()

        try:
            response = {
                "result": classifier_implementation.classify(args)
            }
        except Exception:
            logger.exception("failed to classify object")

            return abort(
                500,
                error="failed to classify object",
                classifier=classifier
            )

        log_msg = "classification request executed successfully: classifier={}"
        logger.info(log_msg.format(classifier))

        return response


class ClassifiersResource(Resource):
    def get(self):
        logger.info("list of usable classifiers requested")

        return current_app.config["CLASSIFIERS"].keys()


class HealthResource(Resource):
    def get(self):
        logger.info("health check requested")

        return {"result": "ok"}


class InformationResource(Resource):
    def get(self):
        logger.info("service information requested")

        return {
            "service": "classifier",
            "version": __VERSION__,
            "host": current_app.config["HOST"],
            "port": current_app.config["PORT"]
        }
