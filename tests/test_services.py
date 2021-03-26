from unittest import TestCase, mock

from mongoengine import disconnect

from src.data.database import start_database
from src.models.complaint import ModificationComplaint
from src.services import complaint_service


class TestService(TestCase):

    @classmethod
    def setUpClass(cls):
        disconnect()
        start_database()

    @mock.patch('src.services.complaint_service.assert_article_existing_and_return')  # nothing to do
    def test_created_read_update(self, mock_article_existing_and_return):
        one = complaint_service.create(
            {"mobile": 123456, "token": "mock"},
            ModificationComplaint(barcode='123456', description='123456'))
        complaint = complaint_service.read(123456, "ADMIN", one.id)
        self.assertIsNotNone(complaint)
        self.assertTrue(complaint.opened)

        complaint_service.update(
            {"token": "mock", 'mobile': 123456, 'name': 'admin', 'role': 'ADMIN'}, one.id,
            ModificationComplaint(barcode='123456', description='123456', reply='update'))
        complaint = complaint_service.read(123456, "ADMIN", one.id)
        self.assertEqual('update', complaint.reply)
        self.assertFalse(complaint.opened)
        mock_article_existing_and_return.assert_called()
