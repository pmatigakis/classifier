from flask import current_app
from flask_restful import Resource, abort

import reqparsers


class ClassifierResource(Resource):
    def post(self, classifier):
        current_app.logger.info(
            "running classifier: classifier={}".format(classifier))

        classifier_implementation = current_app.config["CLASSIFIERS"] \
                                               .get(classifier)

        if classifier_implementation is None:
            current_app.logger.warning(
                "unknown classifier: classifier={}".format(classifier))

            return abort(
                404,
                error="unknown classifier",
                classifier=classifier
            )

        args = reqparsers.classifier_data.parse_args()

        try:
            return {
                "result": classifier_implementation.classify(args)
            }
        except Exception:
            current_app.logger.exception("failed to classify object")

            return abort(
                500,
                error="failed to classify object",
                classifier=classifier
            )


class ClassifiersResource(Resource):
    def get(self):
        return current_app.config["CLASSIFIERS"].keys()


class HealthResource(Resource):
    def get(self):
        return {"result": "ok"}
