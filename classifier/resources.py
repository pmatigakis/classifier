import logging

from flask import current_app
from flask_restful import Resource, abort

from classifier import reqparsers

from classifier import __VERSION__

logger = logging.getLogger(__name__)


class ClassifierResource(Resource):
    def _handle_unknown_classifier_error(self, classifier):
        logger.warning("unknown classifier: classifier=%s", classifier)

        return abort(
            404,
            error="unknown classifier",
            classifier=classifier
        )

    def _handle_classifier_execution_error(self, classifier):
        log_msg = "error occurred while running classifier: classifier=%s"
        logger.exception(log_msg, classifier)

        return abort(
            500,
            error="failed to classify object",
            classifier=classifier
        )

    def post(self, classifier):
        logger.info("running classifier: classifier=%s", classifier)

        classifier_implementation = current_app.config["CLASSIFIERS"] \
                                               .get(classifier)

        if classifier_implementation is None:
            return self._handle_unknown_classifier_error(classifier)

        args = reqparsers.classifier_data.parse_args()

        try:
            response = {
                "results": classifier_implementation.classify(args)
            }
        except Exception:
            return self._handle_classifier_execution_error(classifier)

        log_msg = "classification request executed successfully: classifier=%s"
        logger.info(log_msg, classifier)

        return response


class ClassifiersResource(Resource):
    def get(self):
        logger.info("list of usable classifiers requested")

        return list(current_app.config["CLASSIFIERS"].keys())


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
