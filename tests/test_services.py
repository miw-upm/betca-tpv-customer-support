import unittest
from mongoengine import connect, disconnect

from src.domain.complaint_service import ComplaintService
from src.domain.models import ModificationComplaint


class TestService(unittest.TestCase):
    def setUp(self):
        self.service = ComplaintService()
        disconnect()
        connect('mongoenginetest', host='mongomock://localhost')

    def tearDown(self) -> None:
        disconnect()

    def test_created_read(self):
        one = self.service.create(ModificationComplaint(mobile=123456, barcode='123456', description='123456'))
        self.assertIsNotNone(self.service.read(one.id))


if __name__ == '__main__':
    unittest.main()
