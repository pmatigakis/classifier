from unittest import TestCase, main

from classifier.exceptions import ClassifierMethodVerificationError
from classifier.ml import Classifier


class ClassifierTests(TestCase):
    def test_fail_to_use_classifier_with_missing_methods(self):
        # this class doesn't contain the required methods
        invalid_classifier = TestCase

        with self.assertRaises(ClassifierMethodVerificationError) as e:
            Classifier(invalid_classifier)

        self.assertEqual(
            e.exception.reason,
            "the classifier doesn't have the 'predict' method"
        )


if __name__ == "__main__":
    main()
