import json

import joblib
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.linear_model import LogisticRegression
from sklearn.multiclass import OneVsRestClassifier


def main():
    with open("dataset.json") as f:
        dataset = json.load(f)

    binarizer = MultiLabelBinarizer()
    targets = binarizer.fit_transform(dataset["targets"])

    classifier = OneVsRestClassifier(LogisticRegression())
    classifier.fit(dataset["data"], targets)

    joblib.dump(binarizer, "binarizer.joblib")
    joblib.dump(classifier, "classifier.joblib")


if __name__ == "__main__":
    main()
