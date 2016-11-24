from unittest import TestCase
from os import path

from classifier.application import create_app
from classifier.models import db, User


class ClassifierTestCase(TestCase):
    def setUp(self):
        configuration_file = path.join(
            path.dirname(path.abspath(__file__)),
            "configuration",
            "settings.py"
        )

        self.app = create_app(configuration_file)

        try:
            db.create_all()
        except Exception:
            self.fail("failed to initialize database")


class ClassifierTestCaseWithMockData(ClassifierTestCase):
    def setUp(self):
        super(ClassifierTestCaseWithMockData, self).setUp()

        self.username = "user1"
        self.password = "password"

        user = User.create(self.username, self.password)

        self.jti = user.jti

        try:
            db.session.commit()
        except Exception:
            db.session.rollback()
            self.fail("failed to create mock data")
