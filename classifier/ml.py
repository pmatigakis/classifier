import logging

import numpy as np
from sklearn.externals import joblib


logger = logging.getLogger(__name__)


def extract_text_data(data):
    return data


class Classifier(object):
    def __init__(self, classifier, data_extractor=None, result_processor=None,
                 binarizer=None, probabilities=False):
        if binarizer is not None:
            binarizer = joblib.load(binarizer)

        classifier = joblib.load(classifier)

        self.data_extractor = data_extractor
        self.classifier = classifier
        self.binarizer = binarizer
        self.result_processor = result_processor
        self.probabilities = probabilities

    def extract_data(self, args):
        if self.data_extractor is None:
            data = np.array([args.data])
        else:
            data = self.data_extractor(args.data)

        return data

    def label_result(self, result):
        result = result[0]

        if self.binarizer:
            if self.probabilities:
                return dict(zip(self.binarizer.classes_, result))
            else:
                return self.binarizer.inverse_transform(np.array([result]))[0]
        else:
            if self.probabilities:
                return dict(zip(self.classifier.classes_, result))
            else:
                return result.tolist()

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
        result = self.label_result(result)
        result = self.process_result(result)

        return result
