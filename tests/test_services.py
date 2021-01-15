from unittest import TestCase, mock

from mongoengine import disconnect

from src.data.database import start_database
from src.domain.complaint_service import complaint_service
from src.domain.models import ModificationComplaint


class TestService(TestCase):

    @classmethod
    def setUpClass(cls):
        disconnect()
        start_database()

    @mock.patch('src.rest_client.core_api.ArticleApi.article_existing', return_value=None)
    def test_created_read(self, article_existing):
        one = complaint_service.create(123456, ModificationComplaint(barcode='123456', description='123456'))
        self.assertIsNotNone(complaint_service.read(123456, one.id))
        article_existing.assert_called()
