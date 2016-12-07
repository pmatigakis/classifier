import logging

import numpy as np
from sklearn.externals import joblib


logger = logging.getLogger(__name__)


def extract_text_data(data):
    return data


class Classifier(object):
    def __init__(self, classifier, data_extractor=None, result_processor=None,
                 binarizer=None):
        if binarizer is not None:
            binarizer = joblib.load(binarizer)

        classifier = joblib.load(classifier)

        self.data_extractor = data_extractor
        self.classifier = classifier
        self.binarizer = binarizer
        self.result_processor = result_processor

    def extract_data(self, args):
        if self.data_extractor is None:
            data = np.array([args.data])
        else:
            data = self.data_extractor(args.data)

        return data

    def label_result(self, result):
        if self.binarizer:
            return self.binarizer.inverse_transform(result)[0]
        else:
            return result[0].tolist()

    def process_result(self, result):
        if self.result_processor is None:
            return result
        else:
            return self.result_processor(result)

    def run_classifier(self, features):
        return self.classifier.predict(features)

    def classify(self, args):
        data = self.extract_data(args)

        result = self.run_classifier(data)
        result = self.label_result(result)
        result = self.process_result(result)

        return result


class ProbabilityClassifier(Classifier):
    def __init__(self, classifier, data_extractor=None, result_processor=None,
                 binarizer=None):
        super(ProbabilityClassifier, self).__init__(
            classifier=classifier,
            data_extractor=data_extractor,
            result_processor=result_processor,
            binarizer=binarizer
        )

    def label_result(self, result):
        result = result[0]

        if self.binarizer:
            return dict(zip(self.binarizer.classes_, result))
        else:
            return dict(zip(self.classifier.classes_, result))

    def run_classifier(self, features):
        return self.classifier.predict_proba(features)
