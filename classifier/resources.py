from flask import current_app
from flask_jwt import jwt_required
from flask_restful import Resource, abort
import numpy as np

import reqparsers


class MultiLabelClassifier(Resource):
    def __init__(self, data_extractor=None, labels=None,
                 feature_extractor=None, feature_selector=None,
                 classifier=None, result_processor=None):
        self.data_extractor = data_extractor
        self.labels = labels
        self.feature_extractor = feature_extractor
        self.feature_selector = feature_selector
        self.classifier = classifier
        self.result_processor = result_processor

    def extract_data(self):
        if self.data_extractor is None:
            args = reqparsers.classifier_data.parse_args()
            data = np.array(args.data)
        else:
            data = self.data_extractor()

        return data

    def extract_features(self, data):
        if self.feature_extractor is None:
            return data
        else:
            return self.feature_extractor.transform(data)

    def select_features(self, data):
        if self.feature_selector is None:
            return data
        else:
            return self.feature_selector.transform(data)

    def parse_labels(self, predicted_labels):
        if self.labels is None:
            return predicted_labels
        else:
            labels = []
            for label_index, label_assigned in enumerate(predicted_labels[0]):
                if label_assigned == 1:
                    labels.append(self.labels[label_index])
            return labels

    def process_result(self, result):
        if self.result_processor is None:
            return result.tolist()
        else:
            return self.result_processor(result)

    def classify(self):
        data = [self.extract_data()]

        features = self.extract_features(data)
        features = self.select_features(features)

        predicted_labels = self.classifier.predict(features)

        result = self.parse_labels(predicted_labels)
        result = self.process_result(result)

        return {
            "result": result
        }

    @jwt_required()
    def post(self):
        try:
            return self.classify()
        except Exception:
            current_app.logger.exception("failed to classify object")

            abort(500, error="failed to classify object")
