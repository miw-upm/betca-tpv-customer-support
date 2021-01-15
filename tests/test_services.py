import unittest

from mongoengine import disconnect

from src.data.database import start_database
from src.domain.complaint_service import ComplaintService, complaint_service
from src.domain.models import ModificationComplaint


class TestService(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        start_database()

    def test_created_read(self):
        one = complaint_service.create(123456, ModificationComplaint(barcode='123456', description='123456'))
        self.assertIsNotNone(complaint_service.read(123456, one.id))

    def tearDown(self) -> None:
        disconnect()
