import json
from unittest import main
from unittest.mock import patch

from common import ClassifierTestCaseWithMockClassifiers
from classifier import __VERSION__
from classifier.ml import Classifier


class ClassificationEndpointTests(ClassifierTestCaseWithMockClassifiers):
    def test_probability_classifier(self):
        client = self.app.test_client()

        data = {
            "data": [[5.4, 3.0, 4.5, 1.5]]
        }

        headers = {
            "Content-Type": "application/json",
        }

        response = client.post(
            "/api/v1/predict/iris_probabilities",
            data=json.dumps(data),
            headers=headers
        )

        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data.decode())
        self.assertIn("results", data)
        self.assertEqual(len(data["results"]), 1)
        self.assertEqual(len(data["results"][0]), 3)
        self.assertAlmostEqual(
            data["results"][0]["Iris-setosa"], 0.01031, 5)
        self.assertAlmostEqual(
            data["results"][0]["Iris-versicolor"], 0.36503, 5)
        self.assertAlmostEqual(
            data["results"][0]["Iris-virginica"], 0.62465, 5)

    def test_classifier(self):
        client = self.app.test_client()

        data = {
            "data": [[5.4, 3.0, 4.5, 1.5]]
        }

        headers = {
            "Content-Type": "application/json",
        }

        response = client.post(
            "/api/v1/predict/iris", data=json.dumps(data), headers=headers)

        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data.decode())

        self.assertDictEqual(
            data,
            {
                "results": ["Iris-virginica"]
            }
        )

    def test_classifier_does_not_exist(self):
        client = self.app.test_client()

        data = {
            "data": [[5.4, 3.0, 4.5, 1.5]]
        }

        headers = {
            "Content-Type": "application/json",
        }

        response = client.post(
            "/api/v1/predict/fail_test",
            data=json.dumps(data),
            headers=headers
        )

        self.assertEqual(response.status_code, 404)

        data = json.loads(response.data.decode())

        self.assertDictEqual(
            data,
            {
                "classifier": "fail_test",
                "error": "unknown classifier"
            }
        )

    @patch.object(Classifier, "classify")
    def test_error_while_running_classification(self, classify_mock):
        classify_mock.side_effect = Exception

        client = self.app.test_client()

        data = {
            "data": [[5.4, 3.0, 4.5, 1.5]]
        }

        headers = {
            "Content-Type": "application/json",
        }

        response = client.post(
            "/api/v1/predict/iris", data=json.dumps(data), headers=headers)

        self.assertEqual(response.status_code, 500)

        data = json.loads(response.data.decode())

        self.assertDictEqual(
            data,
            {
                "error": "failed to classify object",
                "classifier": "iris"
            }
        )


class ClassifiersResourceTests(ClassifierTestCaseWithMockClassifiers):
    def test_get_available_classifiers(self):
        client = self.app.test_client()

        response = client.get("/api/v1/classifiers")

        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data.decode())

        self.assertCountEqual(
            data,
            [
                'iris',
                'iris_probabilities'
             ]
        )


class HealthResourceTests(ClassifierTestCaseWithMockClassifiers):
    def test_get_health(self):
        client = self.app.test_client()

        response = client.get("/service/health")

        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data.decode())

        self.assertDictEqual(data, {"result": "ok"})


class InformationResourceTests(ClassifierTestCaseWithMockClassifiers):
    def test_get_information(self):
        client = self.app.test_client()

        response = client.get("/service/information")

        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data.decode())

        self.assertDictEqual(
            data,
            {
                "host": "127.0.0.1",
                "port": 8022,
                "service": "classifier",
                "version": __VERSION__
            }
        )


if __name__ == "__main__":
    main()
