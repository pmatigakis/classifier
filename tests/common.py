from unittest import TestCase
from os import path

from classifier.application import create_app


class ClassifierTestCase(TestCase):
    settings_file_name = "settings.py"

    def setUp(self):
        configuration_file = path.join(
            path.dirname(path.abspath(__file__)),
            "configuration",
            self.settings_file_name
        )

        self.app = create_app(configuration_file)


class ClassifierTestCaseWithMockClassifiers(ClassifierTestCase):
    settings_file_name = "settings_with_classifier.py"
