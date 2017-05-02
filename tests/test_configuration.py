from unittest import TestCase, main
from os import path

from classifier.application import create_app


class ProductionConfigurationTests(TestCase):
    def test_load_production_configuration(self):
        configuration_file = path.join(
            path.dirname(path.abspath(__file__)),
            "configuration",
            "empty_settings.py"
        )

        app = create_app(configuration_file, "production")

        self.assertFalse(app.config["DEBUG"])
        self.assertFalse(app.config["TESTING"])

        self.assertEqual(app.config["SOME_VALUE"], 1234)

    def test_load_testing_configuration(self):
        configuration_file = path.join(
            path.dirname(path.abspath(__file__)),
            "configuration",
            "empty_settings.py"
        )

        app = create_app(configuration_file, "testing")

        self.assertFalse(app.config["DEBUG"])
        self.assertTrue(app.config["TESTING"])

        self.assertEqual(app.config["SOME_VALUE"], 1234)

    def test_load_development_configuration(self):
        configuration_file = path.join(
            path.dirname(path.abspath(__file__)),
            "configuration",
            "empty_settings.py"
        )

        app = create_app(configuration_file, "development")

        self.assertTrue(app.config["DEBUG"])
        self.assertFalse(app.config["TESTING"])

        self.assertEqual(app.config["SOME_VALUE"], 1234)


if __name__ == "__main__":
    main()
