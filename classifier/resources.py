from flask import current_app
from flask_jwt import jwt_required
from flask_restful import Resource, abort

import reqparsers
from helpers import process_web_page


class ClassifierResource(Resource):
    def __init__(self, document_classifier):
        self._document_classifier = document_classifier

    @jwt_required()
    def post(self):
        args = reqparsers.classification_request.parse_args()

        msg = "classifing content: content_size(%d)"
        current_app.logger.info(msg, len(args.content))

        try:
            classification_response = self._classify(args.content)
        except Exception:
            current_app.logger.exception("content classification failed")
            abort(
                500,
                error="content classification failed"
            )

        return self._send_response(classification_response)

    def _classify(self, contents):
        processed_contents = process_web_page(contents)

        return self._document_classifier.classify(processed_contents)

    def _send_response(self, classification_results, **kwargs):
        response = {
            "result": classification_results
        }

        response.update(**kwargs)

        return response
