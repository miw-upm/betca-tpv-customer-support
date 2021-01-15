from http import HTTPStatus
from unittest import TestCase, mock

import jwt
from fastapi.testclient import TestClient

from src.config import Config
from src.main import app, create_app
from src.rest.resources import COMPLAINTS


def mock_article_existing(barcode):
    print(">>>>>>>MOCK from article_existing, barcode:", barcode)


class TestComplaintResource(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.bearer = "Bearer " + jwt.encode({"user": "666666003", "name": "customer", "role": "CUSTOMER"},
                                            Config.jwt_secret, algorithm="HS256")
        cls.client = TestClient(app)

    def test_search_not_token_forbidden_exception(self):
        response = self.client.get(COMPLAINTS + "/search")
        self.assertEqual(HTTPStatus.FORBIDDEN, response.status_code)

    def test_search_not_role_unauthorized_exception(self):
        bearer = "Bearer " + jwt.encode({"user": "66", "name": "customer", "role": "KK"},
                                        Config.jwt_secret, algorithm="HS256")
        response = self.client.get(COMPLAINTS + "/search", headers={"Authorization": bearer})
        self.assertEqual(HTTPStatus.FORBIDDEN, response.status_code)

    def test_search_invalid_token_unauthorized_exception(self):
        bearer = "Bearer kk" + jwt.encode({"user": "66", "name": "customer", "role": "CUSTOMER"},
                                          Config.jwt_secret, algorithm="HS256")
        response = self.client.get(COMPLAINTS + "/search", headers={"Authorization": bearer})
        self.assertEqual(HTTPStatus.UNAUTHORIZED, response.status_code)

    def test_search_not_included_role_forbidden_exception(self):
        bearer = "Bearer " + jwt.encode({"user": "66", "name": "customer", }, Config.jwt_secret, algorithm="HS256")
        response = self.client.get(COMPLAINTS + "/search", headers={"Authorization": bearer})
        self.assertEqual(HTTPStatus.UNAUTHORIZED, response.status_code)

    def test_search_expired_token_unauthorized_exception(self):
        bearer = "Bearer " + jwt.encode({"exp": 1371720939, "user": "66", "name": "customer", "role": "CUSTOMER"},
                                        Config.jwt_secret, algorithm="HS256")
        response = self.client.get(COMPLAINTS + "/search", headers={"Authorization": bearer})
        self.assertEqual(HTTPStatus.UNAUTHORIZED, response.status_code)

    def __read_all(self):
        response = self.client.get(COMPLAINTS + "/search", headers={"Authorization": self.bearer})
        return response.json()

    def test_search(self):
        complaints = self.__read_all()
        for complaint in complaints:
            self.assertEqual(666666003, complaint['mobile'])  # Complaint(**complaint).mobile)

    @mock.patch('src.rest_client.core_api.ArticleApi.article_existing', side_effect=mock_article_existing)
    def test_create_delete(self, article_existing):
        complaint = {"barcode": "8400000000100", "description": "test"}
        response = self.client.post(COMPLAINTS, json=complaint, headers={"Authorization": self.bearer})
        self.assertEqual(HTTPStatus.OK, response.status_code)
        ide = response.json()['id']
        response = self.client.delete(COMPLAINTS + "/" + ide, headers={"Authorization": self.bearer})
        self.assertEqual(HTTPStatus.OK, response.status_code)
        article_existing.assert_called()  # article_existing.not_called()

    def test_read(self):
        complaint = self.__read_all()[0]
        ide = complaint['id']
        response = self.client.get(COMPLAINTS + "/" + ide, headers={"Authorization": self.bearer})
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertEqual(ide, response.json()['id'])

    def test_update(self):
        complaint = self.__read_all()[0]
        ide = complaint['id']
        complaint['description'] = 'update'
        response = self.client.put(COMPLAINTS + "/" + ide, json=complaint, headers={"Authorization": self.bearer})
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertEqual('update', response.json()['description'])
        complaint['description'] = '123456'
        self.client.put(COMPLAINTS + "/" + ide, json=complaint, headers={"Authorization": self.bearer})
