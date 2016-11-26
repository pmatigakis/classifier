import traceback
import json
from unittest import TestCase
from os import path

from classifier.application import create_app
from classifier.models import db, User


class ClassifierTestCase(TestCase):
    settings_file_name = "settings.py"

    def setUp(self):
        configuration_file = path.join(
            path.dirname(path.abspath(__file__)),
            "configuration",
            self.settings_file_name
        )

        self.app = create_app(configuration_file)

        with self.app.app_context():
            try:
                db.create_all()
            except Exception:
                self.fail("failed to initialize database")

    def authenticate_using_jwt(self, username, password):
        client = self.app.test_client()

        credentials = {
            "username": username,
            "password": password
        }

        headers = {
            "Content-Type": "application/json"
        }

        response = client.post(
            "/auth", data=json.dumps(credentials), headers=headers)

        if response.status_code != 200:
            msg = "failed to authenticate using jwt: status_code({})"
            self.fail(msg.format(response.status_code))

        data = json.loads(response.data)

        return data["access_token"]


class ClassifierTestCaseWithMockData(ClassifierTestCase):
    def setUp(self):
        super(ClassifierTestCaseWithMockData, self).setUp()

        self.username = "user1"
        self.password = "password"

        with self.app.app_context():
            user = User.create(self.username, self.password)

            self.jti = user.jti

            try:
                db.session.commit()
            except Exception:
                db.session.rollback()
                traceback.print_exc()
                self.fail("failed to create mock data")


class ClassifierTestCaseWithMockClassifiers(ClassifierTestCaseWithMockData):
    settings_file_name = "settings_with_classifier.py"
