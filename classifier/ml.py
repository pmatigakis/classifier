import logging

import numpy as np
import joblib


logger = logging.getLogger(__name__)


def extract_text_data(data):
    return data


class Classifier(object):
    def __init__(self, classifier, binarizer=None, probabilities=False):
        self.probabilities = probabilities

        self.classifier = self._load_component(classifier)
        self.binarizer = self._load_component(binarizer)

    def _load_component(self, component):
        if isinstance(component, str):
            return joblib.load(component)
        else:
            return component

    def run_classifier(self, data):
        return (
            self.classifier.predict_proba(data) if self.probabilities
            else self.classifier.predict(data)
        )

    def _create_probabilities_response(self, classification_results):
        classes = (
            self.binarizer.classes_
            if self.binarizer
            else self.classifier.classes_
        )

        return [
            dict(zip(classes, result))
            for result in classification_results
        ]

    def _create_result_response(self, classification_results):
        if self.binarizer:
            classification_results = self.binarizer.inverse_transform(
                classification_results)

        return (
            classification_results.tolist()
            if not isinstance(classification_results, list)
            else classification_results
        )

    def _create_response(self, classification_results):
        if self.probabilities:
            return self._create_probabilities_response(classification_results)
        else:
            return self._create_result_response(classification_results)

    def classify(self, args):
        data = np.array(args.data)

        classification_results = self.run_classifier(data)
        response = self._create_response(classification_results)

        return response
