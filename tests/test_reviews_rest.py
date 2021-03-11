from http import HTTPStatus
from unittest import TestCase, mock

import jwt
from fastapi.testclient import TestClient

from src.api.review_resource import REVIEWS
from src.config import config
from src.main import app
from src.models.article import Article
from src.models.review import Review


def _bearer(**payload):
    payload.setdefault("user", "666666003")
    payload.setdefault("name", "customer")
    return "Bearer " + jwt.encode(payload, config.JWT_SECRET, algorithm="HS256")


class TestReviewResource(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.bearer = _bearer(role="CUSTOMER")
        cls.client = TestClient(app)

    def test_search_not_token_forbidden_exception(self):
        response = self.client.get(REVIEWS + "/search")
        self.assertEqual(HTTPStatus.FORBIDDEN, response.status_code)

    def test_search_not_role_unauthorized_exception(self):
        bearer = _bearer(role="KK")
        response = self.client.get(REVIEWS + "/search", headers={"Authorization": bearer})
        self.assertEqual(HTTPStatus.FORBIDDEN, response.status_code)

    def test_search_invalid_token_unauthorized_exception(self):
        bearer = _bearer(role="CUSTOMER") + "kkkk"
        response = self.client.get(REVIEWS + "/search", headers={"Authorization": bearer})
        self.assertEqual(HTTPStatus.UNAUTHORIZED, response.status_code)

    def test_search_not_included_role_forbidden_exception(self):
        bearer = _bearer()
        response = self.client.get(REVIEWS + "/search", headers={"Authorization": bearer})
        self.assertEqual(HTTPStatus.UNAUTHORIZED, response.status_code)

    def test_search_expired_token_unauthorized_exception(self):
        bearer = _bearer(exp=1371720939, role="CUSTOMER")
        response = self.client.get(REVIEWS + "/search", headers={"Authorization": bearer})
        self.assertEqual(HTTPStatus.UNAUTHORIZED, response.status_code)

    def __read_all(self):
        response = self.client.get(REVIEWS + "/search", headers={"Authorization": self.bearer})
        return response.json()

    @mock.patch('src.services.review_service.assert_article_existing_and_return',
                return_value=Article(barcode="00000002", description="Test", retailPrice=1.5))
    def test_create(self, mock_article_existing_and_return):
        creation_review = Review(barcode="00000002", score=1.5)
        response = self.client.post(REVIEWS, json=creation_review.dict(), headers={"Authorization": self.bearer})
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertEqual(creation_review.barcode, response.json()['article']['barcode'])
        self.assertEqual(creation_review.score, response.json()['score'])
        mock_article_existing_and_return.assert_called()

    @mock.patch('src.services.review_service.assert_article_existing_and_return',
                return_value=Article(barcode="8400000000017", description="Mock most rated article", retailPrice=30))
    def test_update(self, mock_article_existing_and_return):
        review = self.__read_all()[0]
        update_review = Review(**review, barcode=review['article']['barcode'])
        ide = update_review.id
        update_review.opinion = 'Changed'
        update_review.score = 4.5
        response = self.client.put(REVIEWS + "/" + ide,
                                   json=update_review.dict(), headers={"Authorization": self.bearer})
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertIsNotNone(response.json()['article'])
        self.assertEqual('Changed', response.json()['opinion'])
        self.assertEqual(4.5, response.json()['score'])
        mock_article_existing_and_return.assert_called()

    def test_search(self):
        reviews = self.__read_all()
        for review in reviews:
            self.assertIsNotNone(review)

    def test_top_articles(self):
        response = self.client.get(REVIEWS + "/topArticles")
        self.assertEqual(HTTPStatus.OK, response.status_code)
        for article in response.json():
            self.assertIsNotNone(article)
