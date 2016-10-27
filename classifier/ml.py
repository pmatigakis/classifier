class MultiLabelDocumentClassifier(object):
    def __init__(self, classes, feature_extractor, classifier):
        self.classes = classes
        self.feature_extractor = feature_extractor
        self.classifier = classifier

    def classify(self, document):
        data = self.feature_extractor.transform([document])

        result = self.classifier.predict(data)

        labels = []
        for label_index, label_assigned in enumerate(result[0]):
            if label_assigned == 1:
                labels.append(self.classes[label_index])

        return labels


class DocumentLabelProcessor(MultiLabelDocumentClassifier):
    def __init__(self, label_classifier):
        self.label_classifier = label_classifier

    def classify(self, document):
        labels = self.label_classifier.classify(document)

        return labels


class Classifiers(object):
    def __init__(self, app=None):
        if app is not None:
            self.init__app(app)

    def init__app(self, app):
        self._classifiers = {}

    def add_classifier(self, name, classifier):
        self._classifiers[name] = classifier

    def classify(self, document):
        response = {}

        for classifier_name, classifier in self._classifiers.items():
            results = classifier.classify(document)

            response[classifier_name] = results

        return response
