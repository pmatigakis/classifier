import json
from unittest import main

from common import ClassifierTestCaseWithMockClassifiers


class ClassificationEndpointTests(ClassifierTestCaseWithMockClassifiers):
    def test_call_classification_endpoint(self):
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
            "/api/labels", data=json.dumps(data), headers=headers)

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


if __name__ == "__main__":
    main()
