import unittest

from fastapi.testclient import TestClient

from main import app


class RootRouteTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_root_returns_welcome_message(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertIn("Journal API", response.json()["message"])
