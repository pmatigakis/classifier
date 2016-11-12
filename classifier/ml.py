import logging


logger = logging.getLogger(__name__)


class MultiLabelDocumentClassifier(object):
    def __init__(self, classes, feature_extractor, feature_selector,
                 classifier):
        self.classes = classes
        self.feature_extractor = feature_extractor
        self.feature_selector = feature_selector
        self.classifier = classifier

    def classify(self, document):
        data = self.feature_extractor.transform([document])
        data = self.feature_selector.transform(data)

        result = self.classifier.predict(data)

        labels = []
        for label_index, label_assigned in enumerate(result[0]):
            if label_assigned == 1:
                labels.append(self.classes[label_index])

        return labels


class Classifiers(object):
    def __init__(self):
        self._classifiers = {}

    def add_classifier(self, name, classifier):
        self._classifiers[name] = classifier

    def classify(self, document):
        response = {}

        for classifier_name, classifier in self._classifiers.items():
            logger.debug(
                "classifing document: classifier(%s)", classifier_name)

            results = classifier.classify(document)

            response[classifier_name] = results

        return response
