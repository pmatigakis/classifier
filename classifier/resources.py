from os import path

import requests
from flask import current_app
from flask_jwt import jwt_required
from flask_restful import Resource
from sklearn.externals import joblib

import reqparsers
from helpers import process_web_page


class QueryResource(Resource):
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

        contents = process_web_page(response.text)

        data_path = current_app.config["DATA_PATH"]

        class_ids = joblib.load(path.join(data_path, "class_ids.pickle"))
        class_ids = {class_id: klass for klass, class_id in class_ids.items()}

        feature_extractor = joblib.load(
            path.join(data_path, "feature_extractor.pickle"))

        clf = joblib.load(path.join(data_path, "classifier.pickle"))

        data = feature_extractor.transform([contents])

        result = clf.predict(data)

        labels = []
        for label_index, label_assigned in enumerate(result[0]):
            if label_assigned == 1:
                labels.append(class_ids[label_index])

        categories = []

        for label in labels:
            items = label.split("_")
            if items[0] == "category":
                category = " ".join(items[1:])
                categories.append(category)

        return {
            "url": args.url,
            "categories": categories
        }
