from flask_restful import reqparse


url_parser = reqparse.RequestParser()
url_parser.add_argument("url", required=True, help="the url to classify")


classification_request = reqparse.RequestParser()
classification_request.add_argument(
    "content", required=True, help="The content to classify")


classifier_data = reqparse.RequestParser()
classifier_data.add_argument(
    "data", required=True, help="The data to classify")
