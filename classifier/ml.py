import logging

import numpy as np
from sklearn.externals import joblib


logger = logging.getLogger(__name__)


def extract_text_data(data):
    return data


class Classifier(object):
    def __init__(self, classifier, data_extractor=None, feature_extractor=None,
                 feature_selector=None, result_processor=None):
        if feature_extractor is not None:
            feature_extractor = joblib.load(feature_extractor)

        if feature_selector is not None:
            feature_selector = joblib.load(feature_selector)

        classifier = joblib.load(classifier)

        self.data_extractor = data_extractor
        self.feature_extractor = feature_extractor
        self.feature_selector = feature_selector
        self.classifier = classifier
        self.result_processor = result_processor


class MultiLabelClassifier(Classifier):
    def __init__(self, classifier, binarizer, **kwargs):
        super(MultiLabelClassifier, self).__init__(classifier, **kwargs)

        self.binarizer = joblib.load(binarizer)

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

    def parse_labels(self, predicted_labels):
        if self.binarizer is None:
            return predicted_labels.tolist()
        else:
            return dict(zip(self.binarizer.classes_, predicted_labels))

    def process_result(self, result):
        if self.result_processor is None:
            return result
        else:
            return self.result_processor(result)

    def classify(self, args):
        data = self.extract_data(args)

        features = self.extract_features(data)
        features = self.select_features(features)

        predicted_labels = self.classifier.predict_proba(features)
        # the result should be only one row because we allow one row for the
        # classification data
        predicted_labels = predicted_labels[0]

        result = self.parse_labels(predicted_labels)
        result = self.process_result(result)

        return result
