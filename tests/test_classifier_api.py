import json
from unittest import main

from common import ClassifierTestCaseWithMockClassifiers


class ClassificationEndpointTests(ClassifierTestCaseWithMockClassifiers):
    def test_probability_multilabel_classifier(self):
        access_token = self.authenticate_using_jwt(
            self.username, self.password)

        client = self.app.test_client()

        data = {
            "data": [1, 1]
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": "JWT {}".format(access_token)
        }

        response = client.post(
            "/api/v1/predict/multilabel_with_binarizer",
            data=json.dumps(data),
            headers=headers
        )

        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data)

        self.assertDictEqual(
            data,
            {
                "result": {
                    'label_1': 0.7678530630986858,
                    'label_2': 0.2321469369013142
                }
            }
        )

    def test_probability_multilabel_classifier_no_binarizer(self):
        access_token = self.authenticate_using_jwt(
            self.username, self.password)

        client = self.app.test_client()

        data = {
            "data": [1, 1]
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": "JWT {}".format(access_token)
        }

        response = client.post(
            "/api/v1/predict/multilabel",
            data=json.dumps(data),
            headers=headers
        )

        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data)

        self.assertDictEqual(
            data,
            {
                "result": {
                    '0': 0.7678530630986858,
                    '1': 0.2321469369013142
                }
            }
        )

    def test_classifier(self):
        access_token = self.authenticate_using_jwt(
            self.username, self.password)

        client = self.app.test_client()

        data = {
            "data": [5.4, 3.0, 4.5, 1.5]
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": "JWT {}".format(access_token)
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

    def test_multilabel_classifier_with_binarizer(self):
        access_token = self.authenticate_using_jwt(
            self.username, self.password)

        client = self.app.test_client()

        data = {
            "data": [6.4, 3.2, 5.3, 2.3]
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": "JWT {}".format(access_token)
        }

        response = client.post(
            "/api/v1/predict/iris_multilabel_with_binarizer",
            data=json.dumps(data),
            headers=headers
        )

        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data)

        self.assertDictEqual(
            data,
            {
                "result": ["Iris-virginica"]
            }
        )

    def test_classifier_with_data_extractor(self):
        access_token = self.authenticate_using_jwt(
            self.username, self.password)

        client = self.app.test_client()

        data = {
            "data": [5.4, 3.0, 4.5, 1.5]
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": "JWT {}".format(access_token)
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
        access_token = self.authenticate_using_jwt(
            self.username, self.password)

        client = self.app.test_client()

        data = {
            "data": [5.4, 3.0, 4.5, 1.5]
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": "JWT {}".format(access_token)
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


if __name__ == "__main__":
    main()
