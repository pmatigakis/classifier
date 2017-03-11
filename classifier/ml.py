import logging

import numpy as np
from sklearn.externals import joblib


logger = logging.getLogger(__name__)


def extract_text_data(data):
    return data


class Classifier(object):
    def __init__(self, classifier, data_extractor=None, result_processor=None,
                 probabilities=False):
        classifier = joblib.load(classifier)

        self.data_extractor = data_extractor
        self.classifier = classifier
        self.result_processor = result_processor
        self.probabilities = probabilities

    def extract_data(self, args):
        if self.data_extractor is None:
            data = np.array([args.data])
        else:
            data = self.data_extractor(args.data)

        return data

    def process_result(self, result):
        if self.result_processor is None:
            return result
        else:
            return self.result_processor(result)

    def run_classifier(self, data):
        if self.probabilities:
            return self.classifier.predict_proba(data)
        else:
            return self.classifier.predict(data)

    def classify(self, args):
        data = self.extract_data(args)

        result = self.run_classifier(data)

        # TODO: the classifier will assume that only one item will be
        # classified so it will only expect one result. This will change in the
        # future so that multiple items can be classified
        result = result[0]
        if self.probabilities:
            result = dict(zip(self.classifier.classes_, result))
        else:
            result = result.tolist()

        result = self.process_result(result)

        return result
