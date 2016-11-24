from unittest import TestCase, main
from os import path

from flask import Flask

from classifier.application import create_app


class ApplicationCreationTests(TestCase):
    def test_create_app(self):
        configuration_file = path.join(
            path.dirname(path.abspath(__file__)),
            "configuration",
            "settings.py"
        )

        app = create_app(configuration_file)

        self.assertIsNotNone(app)
        self.assertIsInstance(app, Flask)


if __name__ == "__main__":
    main()
