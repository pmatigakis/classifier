import logging

import numpy as np
from sklearn.externals import joblib


logger = logging.getLogger(__name__)


def extract_text_data(data):
    return data


class Classifier(object):
    def __init__(self, classifier, data_extractor=None, feature_extractor=None,
                 feature_selector=None, result_processor=None, binarizer=None):
        if feature_extractor is not None:
            feature_extractor = joblib.load(feature_extractor)

        if feature_selector is not None:
            feature_selector = joblib.load(feature_selector)

        if binarizer is not None:
            binarizer = joblib.load(binarizer)

        classifier = joblib.load(classifier)

        self.data_extractor = data_extractor
        self.feature_extractor = feature_extractor
        self.feature_selector = feature_selector
        self.classifier = classifier
        self.binarizer = binarizer
        self.result_processor = result_processor

    def extract_data(self, args):
        if self.data_extractor is None:
            data = np.array([args.data])
        else:
            data = self.data_extractor(args.data)

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

    def label_result(self, result):
        if self.binarizer:
            # TODO: temporary fix
            return self.binarizer.inverse_transform(np.array([result]))[0]
        else:
            return result

    def process_result(self, result):
        if self.result_processor is None:
            return result
        else:
            return self.result_processor(result)

    def run_classifier(self, features):
        return self.classifier.predict(features)

    def classify(self, args):
        data = self.extract_data(args)

        features = self.extract_features(data)
        features = self.select_features(features)

        result = self.run_classifier(features)
        # the result should be only one row because we allow one row for the
        # classification data
        result = result[0].tolist()

        result = self.label_result(result)

        result = self.process_result(result)

        return result


class ProbabilityClassifier(Classifier):
    def __init__(self, classifier, data_extractor=None, feature_extractor=None,
                 feature_selector=None, result_processor=None, binarizer=None):
        super(ProbabilityClassifier, self).__init__(
            classifier=classifier,
            data_extractor=data_extractor,
            feature_extractor=feature_extractor,
            feature_selector=feature_selector,
            result_processor=result_processor,
            binarizer=binarizer
        )

    def label_result(self, result):
        if self.binarizer:
            return dict(zip(self.binarizer.classes_, result))
        else:
            return dict(zip(self.classifier.classes_, result))

    def run_classifier(self, features):
        return self.classifier.predict_proba(features)
