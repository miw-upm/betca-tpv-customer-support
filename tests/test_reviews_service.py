from unittest import TestCase, mock

from fastapi import HTTPException
from mongoengine import disconnect

from src.data.database import start_database
from src.models.article import Article
from src.models.review import Review
from src.services import review_service


class TestReviewsService(TestCase):

    @classmethod
    def setUpClass(cls):
        disconnect()
        start_database()

    @mock.patch('src.services.review_service.assert_article_existing_and_return',
                return_value=Article(barcode="123456", description="Mock", retailPrice=4.5))
    def test_create_read(self, mock_article_existing_and_return):
        review_creation = review_service.create(
            {"mobile": 123456, "token": "mock"},
            Review(barcode="123456", score=1.5))
        ddbb_review = review_service.read(123456, review_creation.id)
        self.assertIsNotNone(ddbb_review)
        self.assertEqual(review_creation.article.barcode, ddbb_review.barcode)
        mock_article_existing_and_return.assert_called()

    @mock.patch('src.services.review_service.assert_article_existing_and_return',
                return_value=Article(barcode="123456", description="Mock", retailPrice=4.5))
    def test_create_read_forbidden(self, mock_article_existing_and_return):
        review_creation = review_service.create(
            {"mobile": 123456, "token": "mock"},
            Review(barcode="123456", score=1.5))
        self.assertRaises(HTTPException, review_service.read, 123, review_creation.id)
        mock_article_existing_and_return.assert_called()
