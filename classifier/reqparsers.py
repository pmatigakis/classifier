from flask_restful import reqparse


url_parser = reqparse.RequestParser()
url_parser.add_argument("url", required=True, help="the url to classify")
