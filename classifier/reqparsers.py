from flask_restful import reqparse


classifier_data = reqparse.RequestParser()
classifier_data.add_argument(
    "data",
    required=True,
    help="The data to classify",
    type=list,
    location='json'
)
