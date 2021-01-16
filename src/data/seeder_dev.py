import logging
from datetime import datetime

from src.data.complaint_data import ComplaintDocument


def delete_all_and_seed_database():
    complaints = [
        ComplaintDocument(mobile=666666003, barcode="8400000000017", description="123456",
                          registration_date=datetime.now()),
        ComplaintDocument(mobile=666666003, barcode="8400000000024", description="123456",
                          registration_date=datetime.now()),
        ComplaintDocument(mobile=666666003, barcode="8400000000031", description="123456",
                          registration_date=datetime.now()),
        ComplaintDocument(mobile=666666004, barcode="8400000000024", description="123456",
                          registration_date=datetime.now()),
        ComplaintDocument(mobile=666666005, barcode="8400000000048", description="123456",
                          registration_date=datetime.now()),
    ]
    logging.info("Delete all and seed database... Complaint")
    ComplaintDocument.drop_collection()

    ComplaintDocument.objects.insert(complaints)

