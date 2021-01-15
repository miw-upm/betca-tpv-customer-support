from datetime import datetime

from src.data.documents import MongoComplaint


def delete_all_and_seed_database():
    complaints = [
        MongoComplaint(mobile=666666003, barcode="8400000000017", description="123456",
                       registration_date=datetime.now()),
        MongoComplaint(mobile=666666003, barcode="8400000000024", description="123456",
                       registration_date=datetime.now()),
        MongoComplaint(mobile=666666003, barcode="8400000000031", description="123456",
                       registration_date=datetime.now()),
        MongoComplaint(mobile=666666004, barcode="8400000000024", description="123456",
                       registration_date=datetime.now()),
        MongoComplaint(mobile=666666005, barcode="8400000000048", description="123456",
                       registration_date=datetime.now()),
    ]
    MongoComplaint.drop_collection()
    print("Seeder Database... Complaint")
    MongoComplaint.objects.insert(complaints)
