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
                raise ClassifierMethodVerificationError(method)

    def run_classifier(self, data):
        if self.probabilities:
            return self.classifier.predict_proba(data)
        else:
            return self.classifier.predict(data)

    def classify(self, args):
        data = np.array(args.data)

        results = self.run_classifier(data)

        if self.probabilities:
            results = [
                dict(zip(self.classifier.classes_, result))
                for result in results
            ]
        else:
            results = results.tolist()

        return results
