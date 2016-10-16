import requests
from flask import Flask
from flask_restful import Resource, reqparse, Api
from bs4 import BeautifulSoup
from sklearn.externals import joblib

import settings


url_parser = reqparse.RequestParser()
url_parser.add_argument("url", required=True, help="the url to classify")


def process_web_page(content):
    soup = BeautifulSoup(content, 'html.parser')
    [s.extract() for s in soup.findAll("script")]
    [s.extract() for s in soup.findAll("style")]
    return soup.get_text()


class LabelsResource(Resource):
    def get(self):
        args = url_parser.parse_args()

        headers = {
            "User-Agent": settings.USER_AGENT
        }

        response = requests.get(
            args.url,
            verify=settings.VERIFY_SSL,
            timeout=settings.REQUEST_TIMEOUT,
            headers=headers
        )

        if response.status_code != 200:
            return {
                "error": "invalid response status code",
                "status_code": response.status_code,
                "url": args.url
            }

        contents = process_web_page(response.text)

        class_ids = joblib.load("data/class_ids.pickle")
        class_ids = {class_id: klass for klass, class_id in class_ids.items()}

        feature_extractor = joblib.load("data/feature_extractor.pickle")

        clf = joblib.load("data/classifier.pickle")

        data = feature_extractor.transform([contents])

        result = clf.predict(data)

        labels = []
        for label_index, label_assigned in enumerate(result[0]):
            if label_assigned == 1:
                labels.append(class_ids[label_index])

        return {
            "url": args.url,
            "labels": labels
        }


def main():
    app = Flask(__name__)

    app.config.from_pyfile("settings.py")

    api = Api(app)

    api.add_resource(LabelsResource, "/api/v1/labels")

    app.run(port=settings.SERVER_PORT)

if __name__ == "__main__":
    main()
