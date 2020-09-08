from unittest import TestCase

from api import app


class BaseTestAPI(TestCase):
    """
    Base Class to API Tests
    """
    def setUp(self):
        self.app = app
        self.app.testing = True
        self.app_context = self.app.test_request_context()
        self.app_context.push()
        self.client = self.app.test_client()
