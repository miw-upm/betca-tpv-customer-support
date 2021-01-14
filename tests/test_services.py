import unittest
from mongoengine import connect, disconnect

from src.domain.complaint_service import ComplaintService
from src.domain.models import ModificationComplaint


class TestService(unittest.TestCase):
    def setUp(self):
        self.service = ComplaintService()
        disconnect()
        connect('mongoenginetest', host='mongomock://localhost')

    def test_created_read(self):
        one = self.service.create(123456, ModificationComplaint(barcode='123456', description='123456'))
        self.assertIsNotNone(self.service.read(123456,one.id))

    def tearDown(self) -> None:
        disconnect()