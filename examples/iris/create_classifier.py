import csv

import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.externals import joblib


def main():
    data = []
    target = []

    with open("iris.data") as f:
        csv_reader = csv.reader(f, delimiter=",")

        for row in csv_reader:
            record = [float(item) for item in row[:4]]
            data.append(record)
            target.append(row[4])

    data = np.array(data)

    clf = LogisticRegression()
    clf.fit(data, target)

    joblib.dump(clf, "classifier.pickle")


if __name__ == "__main__":
    main()
