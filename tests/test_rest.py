from http import HTTPStatus
from unittest import TestCase, mock

import jwt
from fastapi.testclient import TestClient

from src.api.complaint_resource import COMPLAINTS
from src.config import config
from src.main import app


def _bearer(**payload):
    payload.setdefault("user", "666666003")
    payload.setdefault("name", "customer")
    return "Bearer " + jwt.encode(payload, config.JWT_SECRET, algorithm="HS256")


class TestComplaintResource(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.bearer = _bearer(role="CUSTOMER")
        cls.client = TestClient(app)

    def test_search_not_token_forbidden_exception(self):
        response = self.client.get(COMPLAINTS + "/search")
        self.assertEqual(HTTPStatus.FORBIDDEN, response.status_code)

    def test_search_not_role_unauthorized_exception(self):
        bearer = _bearer(role="KK")
        response = self.client.get(COMPLAINTS + "/search", headers={"Authorization": bearer})
        self.assertEqual(HTTPStatus.FORBIDDEN, response.status_code)

    def test_search_invalid_token_unauthorized_exception(self):
        bearer = _bearer(role="CUSTOMER") + "kkkk"
        response = self.client.get(COMPLAINTS + "/search", headers={"Authorization": bearer})
        self.assertEqual(HTTPStatus.UNAUTHORIZED, response.status_code)

    def test_search_not_included_role_forbidden_exception(self):
        bearer = _bearer()
        response = self.client.get(COMPLAINTS + "/search", headers={"Authorization": bearer})
        self.assertEqual(HTTPStatus.UNAUTHORIZED, response.status_code)

    def test_search_expired_token_unauthorized_exception(self):
        bearer = _bearer(exp=1371720939, role="CUSTOMER")
        response = self.client.get(COMPLAINTS + "/search", headers={"Authorization": bearer})
        self.assertEqual(HTTPStatus.UNAUTHORIZED, response.status_code)

    def __read_all(self):
        response = self.client.get(COMPLAINTS + "/search", headers={"Authorization": self.bearer})
        return response.json()

    def test_search(self):
        complaints = self.__read_all()
        for complaint in complaints:
            self.assertEqual(666666003, complaint['mobile'])  # Complaint(**complaint).mobile)

    @mock.patch('src.domain.complaint_service.assert_article_existing', return_value=None)
    def test_create_delete(self, mock_article_existing):
        complaint = {"barcode": "8400000000100", "description": "test"}
        response = self.client.post(COMPLAINTS, json=complaint, headers={"Authorization": self.bearer})
        self.assertEqual(HTTPStatus.OK, response.status_code)
        ide = response.json()['id']
        response = self.client.delete(COMPLAINTS + "/" + ide, headers={"Authorization": self.bearer})
        self.assertEqual(HTTPStatus.OK, response.status_code)
        mock_article_existing.assert_called()

    def test_read_not_found_exception(self):
        response = self.client.get(COMPLAINTS + "/ffff6f3201a6f109756abc07", headers={"Authorization": self.bearer})
        self.assertEqual(HTTPStatus.NOT_FOUND, response.status_code)

    def test_read_forbidden(self):
        complaint = self.__read_all()[0]
        ide = complaint['id']
        bearer = _bearer(user="66", role="CUSTOMER")
        response = self.client.get(COMPLAINTS + "/" + ide, headers={"Authorization": bearer})
        self.assertEqual(HTTPStatus.FORBIDDEN, response.status_code)

    def test_read(self):
        complaint = self.__read_all()[0]
        ide = complaint['id']
        response = self.client.get(COMPLAINTS + "/" + ide, headers={"Authorization": self.bearer})
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertEqual(ide, response.json()['id'])

    @mock.patch('src.domain.complaint_service.assert_article_existing', return_value=None)
    def test_update(self, mock_article_existing):
        complaint = self.__read_all()[0]
        ide = complaint['id']
        complaint['description'] = 'update'
        response = self.client.put(COMPLAINTS + "/" + ide, json=complaint, headers={"Authorization": self.bearer})
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertEqual('update', response.json()['description'])
        complaint['description'] = '123456'
        self.client.put(COMPLAINTS + "/" + ide, json=complaint, headers={"Authorization": self.bearer})
        mock_article_existing.assert_called()
