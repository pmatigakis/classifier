import requests
from flask import current_app
from flask_jwt import jwt_required
from flask_restful import Resource

import reqparsers
from helpers import process_web_page


class ClassifierResource(Resource):
    def __init__(self, document_classifier):
        self._document_classifier = document_classifier

    @jwt_required()
    def get(self):
        args = reqparsers.url_parser.parse_args()

        headers = {
            "User-Agent": current_app.config["USER_AGENT"]
        }

        response = requests.get(
            args.url,
            verify=current_app.config["VERIFY_SSL"],
            timeout=current_app.config["REQUEST_TIMEOUT"],
            headers=headers
        )

        if response.status_code != 200:
            return {
                "error": "invalid response status code",
                "status_code": response.status_code,
                "url": args.url
            }

        classification_response = self._classify(response.text)

        return self._send_response(
            classification_response,
            url=args.url,
            status_code=response.status_code
        )

    @jwt_required()
    def post(self):
        args = reqparsers.classification_request.parse_args()

        classification_response = self._classify(args.contents)

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
