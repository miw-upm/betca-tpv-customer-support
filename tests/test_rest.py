import unittest

from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


class TestService(unittest.TestCase):
    def test_read(self):
        response = client.get("/complaints/666")
        self.assertEqual(403, response.status_code)

