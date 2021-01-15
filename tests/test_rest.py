import unittest
from http import HTTPStatus

import jwt
from fastapi.testclient import TestClient
from mongoengine import disconnect, connect

from src.config import Config
from src.domain.models import Complaint
from src.main import app
from src.rest.resources import COMPLAINTS

client = TestClient(app)


class TestComplaintResource(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.bearer = "Bearer " + jwt.encode({"user": "66", "name": "customer", "role": "CUSTOMER"},
                                            Config.jwt_secret, algorithm="HS256")
        disconnect()
        connect('mongoenginetest', host='mongomock://localhost')

    def test_search_not_token_forbidden_exception(self):
        response = client.get(COMPLAINTS + "/search")
        self.assertEqual(HTTPStatus.FORBIDDEN, response.status_code)

    def test_search_not_role_unauthorized_exception(self):
        bearer = "Bearer " + jwt.encode({"user": "66", "name": "customer", "role": "KK"},
                                        Config.jwt_secret, algorithm="HS256")
        response = client.get(COMPLAINTS + "/search", headers={"Authorization": bearer})
        self.assertEqual(HTTPStatus.FORBIDDEN, response.status_code)

    def test_search_invalid_token_unauthorized_exception(self):
        bearer = "Bearer kk" + jwt.encode({"user": "66", "name": "customer", "role": "CUSTOMER"},
                                          Config.jwt_secret, algorithm="HS256")
        response = client.get(COMPLAINTS + "/search", headers={"Authorization": bearer})
        self.assertEqual(HTTPStatus.UNAUTHORIZED, response.status_code)

    def test_search_not_included_role_forbidden_exception(self):
        bearer = "Bearer " + jwt.encode({"user": "66", "name": "customer", }, Config.jwt_secret, algorithm="HS256")
        response = client.get(COMPLAINTS + "/search", headers={"Authorization": bearer})
        self.assertEqual(HTTPStatus.UNAUTHORIZED, response.status_code)

    def test_search_expired_token_unauthorized_exception(self):
        bearer = "Bearer " + jwt.encode({"exp": 1371720939, "user": "66", "name": "customer", "role": "CUSTOMER"},
                                        Config.jwt_secret, algorithm="HS256")
        response = client.get(COMPLAINTS + "/search", headers={"Authorization": bearer})
        self.assertEqual(HTTPStatus.UNAUTHORIZED, response.status_code)

    def test_search(self):
        response = client.get(COMPLAINTS + "/search", headers={"Authorization": self.bearer})
        self.assertEqual(HTTPStatus.OK, response.status_code)
        for complaint in response.json():
            self.assertIsNotNone(complaint['mobile'])
            self.assertIsNotNone(Complaint(**complaint).mobile)

    def test_crud(self):
        complaint = {"barcode": '33333', "description": '123456'}
        response = client.post(COMPLAINTS, json=complaint, headers={"Authorization": self.bearer})
        self.assertEqual(HTTPStatus.OK, response.status_code)
        ide = response.json()['id']
        response = client.get(COMPLAINTS + "/" + ide, headers={"Authorization": self.bearer})
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertEqual(ide, response.json()['id'])
        complaint['description'] = '654321'
        response = client.put(COMPLAINTS + "/" + ide, json=complaint, headers={"Authorization": self.bearer})
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertEqual('654321', response.json()['description'])
        response = client.delete(COMPLAINTS + "/" + ide, headers={"Authorization": self.bearer})
        self.assertEqual(HTTPStatus.OK, response.status_code)
