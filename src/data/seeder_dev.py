import logging
from datetime import datetime

from src.data.complaint_data import ComplaintDocument
from src.data.review_data import ReviewDocument


def delete_all_and_seed_database():
    complaints = [
        ComplaintDocument(
            mobile=666666003, barcode="8400000000017", description="123456", registration_date=datetime.now()),
        ComplaintDocument(
            mobile=666666003, barcode="8400000000024", description="123456", registration_date=datetime.now()),
        ComplaintDocument(
            mobile=666666003, barcode="8400000000031", description="123456", registration_date=datetime.now()),
        ComplaintDocument(
            mobile=666666004, barcode="8400000000024", description="123456", registration_date=datetime.now()),
        ComplaintDocument(
            mobile=666666005, barcode="8400000000048", description="123456", registration_date=datetime.now()),
    ]
    logging.info("Delete all and seed database... ++Complaint")
    ComplaintDocument.drop_collection()
    ComplaintDocument.objects.insert(complaints)

    reviews = [
        ReviewDocument(mobile=66, barcode="8400000000017", score=2.5, opinion="Is ok but not that much"),
        ReviewDocument(mobile=66, barcode="8400000000024", score=5, opinion="Best product"),
        ReviewDocument(mobile=66, barcode="8400000000031", score=0.5, opinion="Really bad"),
        ReviewDocument(mobile=666666003, barcode="8400000000017", score=4, opinion="I like the product"),
        ReviewDocument(mobile=666666003, barcode="8400000000031", score=1.5, opinion="Bad, really bad"),
        ReviewDocument(mobile=666666003, barcode="8400000000048", score=5, opinion="Best product ever"),
        ReviewDocument(mobile=666666004, barcode="8400000000017", score=3.5, opinion="Is ok but I don't like it"),
        ReviewDocument(mobile=666666004, barcode="8400000000031", score=2, opinion="Not what I expected"),
        ReviewDocument(mobile=666666004, barcode="8400000000024", score=5, opinion="I enjoyed it a lot!"),
        ReviewDocument(mobile=666666005, barcode="8400000000048", score=4.5,
                       opinion="Just few things to make it perfect"),
        ReviewDocument(mobile=666666005, barcode="8400000000017", score=3,
                       opinion="Fits what I expected but bad quality"),
        ReviewDocument(mobile=666666005, barcode="8400000000031", score=0.5, opinion="I don't recommend buying it"),
        ReviewDocument(mobile=666666005, barcode="8400000000017", score=4, opinion="Really good"),
    ]
    logging.info("Delete all and seed database... ++Review")
    ReviewDocument.drop_collection()
    ReviewDocument.objects.insert(reviews)
