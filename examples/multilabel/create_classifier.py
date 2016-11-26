from sklearn.preprocessing import LabelBinarizer
from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import LinearSVC
from sklearn.externals import joblib
from sklearn.calibration import CalibratedClassifierCV


def main():
    target = [
        "label_1",
        "label_1",
        "label_1",
        "label_2",
        "label_2",
        "label_2"
    ]

    train = [
        [1, 2],
        [1, 1],
        [2, 1],
        [5, 5],
        [5, 4],
        [4, 5]
    ]

    binarizer = LabelBinarizer()
    binarizer.fit(["label_1", "label_2"])

    target = binarizer.transform(target)

    classifier = OneVsRestClassifier(CalibratedClassifierCV(LinearSVC()))
    classifier.fit(train, target)

    joblib.dump(binarizer, "binarizer.pickle")
    joblib.dump(classifier, "classifier.pickle")


if __name__ == "__main__":
    main()
