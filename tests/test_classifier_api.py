import json
from unittest import main

from mock import patch

from common import ClassifierTestCaseWithMockClassifiers
from classifier.ml import Classifier


class ClassificationEndpointTests(ClassifierTestCaseWithMockClassifiers):
    def test_probability_classifier(self):
        client = self.app.test_client()

        data = {
            "data": [5.4, 3.0, 4.5, 1.5]
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

        data = json.loads(response.data)

        self.assertDictEqual(
            data,
            {
                "result": {
                    'Iris-setosa': 0.010312340747190656,
                    'Iris-versicolor': 0.3650346947203982,
                    'Iris-virginica': 0.6246529645324113
                }
            }
        )

    def test_classifier(self):
        client = self.app.test_client()

        data = {
            "data": [5.4, 3.0, 4.5, 1.5]
        }

        headers = {
            "Content-Type": "application/json",
        }

        response = client.post(
            "/api/v1/predict/iris", data=json.dumps(data), headers=headers)

        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data)

        self.assertDictEqual(
            data,
            {
                "result": "Iris-virginica"
            }
        )

    def test_classifier_with_data_extractor(self):
        client = self.app.test_client()

        data = {
            "data": [5.4, 3.0, 4.5, 1.5, 0.0, 0.0, 0.0]
        }

        headers = {
            "Content-Type": "application/json",
        }

        response = client.post(
            "/api/v1/predict/iris_with_data_extractor",
            data=json.dumps(data),
            headers=headers
        )

        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data)

        self.assertDictEqual(
            data,
            {
                "result": "Iris-virginica"
            }
        )

    def test_classifier_with_result_processor(self):
        client = self.app.test_client()

        data = {
            "data": [5.4, 3.0, 4.5, 1.5]
        }

        headers = {
            "Content-Type": "application/json",
        }

        response = client.post(
            "/api/v1/predict/iris_with_result_processor",
            data=json.dumps(data),
            headers=headers
        )

        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data)

        self.assertDictEqual(
            data,
            {
                "result": {"data": "Iris-virginica"}
            }
        )

    def test_classifier_does_not_exist(self):
        client = self.app.test_client()

        data = {
            "data": [5.4, 3.0, 4.5, 1.5]
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

        data = json.loads(response.data)

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
            "data": [5.4, 3.0, 4.5, 1.5]
        }

        headers = {
            "Content-Type": "application/json",
        }

        response = client.post(
            "/api/v1/predict/iris", data=json.dumps(data), headers=headers)

        self.assertEqual(response.status_code, 500)

        data = json.loads(response.data)

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

        data = json.loads(response.data)

        self.assertItemsEqual(
            data,
            [
                'iris',
                'iris_probabilities',
                'iris_with_result_processor',
                'iris_with_data_extractor'
             ]
        )


class HealthResourceTests(ClassifierTestCaseWithMockClassifiers):
    def test_get_health(self):
        client = self.app.test_client()

        response = client.get("/service/health")

        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data)

        self.assertDictEqual(data, {"result": "ok"})


class InformationResourceTests(ClassifierTestCaseWithMockClassifiers):
    def test_get_information(self):
        client = self.app.test_client()

        response = client.get("/service/information")

        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data)

        self.assertDictEqual(
            data,
            {
                "host": "127.0.0.1",
                "port": 8022,
                "service": "classifier",
                "version": "0.4.0"
            }
        )


if __name__ == "__main__":
    main()
