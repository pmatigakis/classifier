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


class Classifiers(object):
    def __init__(self):
        self._classifiers = {}

    def add_classifier(self, name, classifier):
        self._classifiers[name] = classifier

    def classify(self, document):
        response = {}

        for classifier_name, classifier in self._classifiers.items():
            results = classifier.classify(document)

            response[classifier_name] = results

        return response
