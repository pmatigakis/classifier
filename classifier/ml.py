import logging

import numpy as np
from sklearn.externals import joblib

from classifier.exceptions import ClassifierMethodVerificationError


logger = logging.getLogger(__name__)


def extract_text_data(data):
    return data


class Classifier(object):
    def __init__(self, classifier, probabilities=False):
        if isinstance(classifier, (str, unicode)):
            classifier = joblib.load(classifier)
        else:
            self._verify_classifier_methods(classifier)
            classifier = classifier

        self.classifier = classifier
        self.probabilities = probabilities

    def _verify_classifier_methods(self, classifier):
        required_methods = ["predict", "predict_proba", "classes_"]
        for method in required_methods:
            if not hasattr(classifier, method):
                logger.error("missing method '%s' from classifier", method)

                raise ClassifierMethodVerificationError(method)

    def run_classifier(self, data):
        return (
            self.classifier.predict_proba(data) if self.probabilities
            else self.classifier.predict(data)
        )

    def _create_response(self, classification_results):
        if self.probabilities:
            results = [
                dict(zip(self.classifier.classes_, result))
                for result in classification_results
            ]
        else:
            results = (
                classification_results.tolist()
                if not isinstance(classification_results, list)
                else classification_results
            )

        return results

    def classify(self, args):
        data = np.array(args.data)

        classification_results = self.run_classifier(data)
        response = self._create_response(classification_results)

        return response
