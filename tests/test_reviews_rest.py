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


def mock_articles(arg1, arg2) -> [Article]:
    return [Article(barcode="8400000000017", description="Mock most rated article", retailPrice=30),
            Article(barcode="8400000000018", description="Mock", retailPrice=30),
            Article(barcode="8400000000019", description="Mock 2", retailPrice=30)]


def mock_assert_article_existing_and_return(token, barcode) -> Article:
    switcher = {
        "8400000000017": Article(barcode="8400000000017", description="Mock most rated article", retailPrice=30),
        "8400000000024": Article(barcode="8400000000024",
                                 description="Mock second most rated article", retailPrice=5, stock=15),
        "8400000000031": Article(barcode="8400000000031", description="Mock third most rated article", retailPrice=305),
        "8400000000048": Article(barcode="8400000000048", description="Nothing", retailPrice=305),
        "8400000000055": Article(barcode="8400000000055", description="Another article", retailPrice=305),
        "8400000000079": Article(barcode="8400000000079", description="Another of another article", retailPrice=305),
        "8400000000086": Article(barcode="8400000000086", description="Look at this article", retailPrice=305)
    }
    default_article = Article(barcode="8400000000017", description="Mock most rated article", retailPrice=30)
    return switcher.get(barcode, default_article)


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

    @mock.patch('src.services.review_service.get_all_bought_articles', side_effect=mock_articles)
    def __read_all(self, get_all_bought_articles):
        bearer = _bearer(user="66", role="CUSTOMER")
        response = self.client.get(REVIEWS + "/search", headers={"Authorization": bearer})
        get_all_bought_articles.assert_called()
        return response.json()

    @mock.patch('src.services.review_service.assert_article_existing_and_return',
                side_effect=mock_assert_article_existing_and_return)
    def test_create(self, mock_article_existing_and_return):
        creation_review = Review(barcode="8400000000031", score=1.5)
        response = self.client.post(REVIEWS, json=creation_review.dict(), headers={"Authorization": self.bearer})
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertEqual(creation_review.barcode, response.json()['article']['barcode'])
        self.assertEqual(creation_review.score, response.json()['score'])
        mock_article_existing_and_return.assert_called()

    @mock.patch('src.services.review_service.assert_article_existing_and_return',
                side_effect=mock_assert_article_existing_and_return)
    def test_update(self, mock_article_existing_and_return):
        review = self.__read_all()[0]
        update_review = Review(**review, barcode=review['article']['barcode'])
        ide = update_review.id
        update_review.opinion = 'Changed'
        update_review.score = 4.5
        bearer = _bearer(user="66", role="CUSTOMER")
        response = self.client.put(REVIEWS + "/" + ide,
                                   json=update_review.dict(), headers={"Authorization": bearer})
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertIsNotNone(response.json()['article'])
        self.assertEqual('Changed', response.json()['opinion'])
        self.assertEqual(4.5, response.json()['score'])
        mock_article_existing_and_return.assert_called()

    @mock.patch('src.services.review_service.assert_article_existing_and_return',
                side_effect=mock_assert_article_existing_and_return)
    def test_search(self, assert_article_existing_and_return):
        reviews = self.__read_all()
        for review in reviews:
            self.assertIsNotNone(review)
        assert_article_existing_and_return.assert_called()

    @mock.patch('src.services.review_service.assert_article_existing_and_return',
                side_effect=mock_assert_article_existing_and_return)
    def test_top_articles(self, assert_article_existing_and_return):
        response = self.client.get(REVIEWS + "/topArticles", headers={"Authorization": self.bearer})
        self.assertEqual(HTTPStatus.OK, response.status_code)
        articles = response.json()
        for article in articles:
            self.assertIsNotNone(article)
        self.assertEqual("8400000000024", articles[0]['barcode'])
        self.assertEqual("8400000000017", articles[1]['barcode'])
        self.assertEqual("8400000000031", articles[2]['barcode'])
        assert_article_existing_and_return.assert_called()
