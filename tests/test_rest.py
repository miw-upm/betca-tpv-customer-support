import unittest
from http import HTTPStatus

from fastapi.testclient import TestClient

from src.domain.models import Complaint
from src.main import app

client = TestClient(app)


class TestComplaintResource(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.bearer = "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJuYmYiOjE2MTA2MzY2ODEsInJvbGUiOiJDVVNUT01FUiI" \
                     "sImlzcyI6ImVzLXVwbS11cG0iLCJuYW1lIjoiY3VzdG9tZXIiLCJleHAiOjE2MTA2NzI2ODEsImlhdCI6MTYxMDYzNj" \
                     "Y4MSwidXNlciI6IjY2In0.sDlkuw1oN2la6_-QQ-u8CMTvoRC2zPWKMXHfyRVesR8"

    def test_search_exception(self):
        response = client.get("/complaints/search")
        self.assertEqual(HTTPStatus.FORBIDDEN, response.status_code)

    def test_search(self):
        response = client.get("/complaints/search", headers={"Authorization": self.bearer})
        self.assertEqual(HTTPStatus.OK, response.status_code)
        for complaint in response.json():
            self.assertIsNotNone(complaint['mobile'])
            self.assertIsNotNone(Complaint(**complaint).mobile)

    def test_crud(self):
        complaint = {"mobile": 66, "barcode": '33333', "description": '123456'}
        response = client.post("/complaints", json=complaint, headers={"Authorization": self.bearer})
        self.assertEqual(HTTPStatus.OK, response.status_code)
        ide = response.json()['id']
        response = client.get("/complaints/" + ide, headers={"Authorization": self.bearer})
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertEqual(ide, response.json()['id'])
        complaint['description'] = '654321'
        response = client.put("/complaints/" + ide, json=complaint, headers={"Authorization": self.bearer})
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertEqual('654321', response.json()['description'])
        response = client.delete("/complaints/" + ide, headers={"Authorization": self.bearer})
        self.assertEqual(HTTPStatus.OK, response.status_code)
