from datetime import datetime

from src.data.documents import MongoComplaint
from .models import Complaint, ModificationComplaint


class ComplaintService:

    def __init__(self):  # constructor
        print('Creating a ComplaintService')

    def find(self):
        complaints = []
        for item in MongoComplaint.objects:
            complaints.append(Complaint(**item.dict()))
        return complaints

    def create(self, modification_complaint: ModificationComplaint):
        mongo_complaint = MongoComplaint(**modification_complaint.dict())
        mongo_complaint.registration_date = datetime.now()
        return Complaint(**mongo_complaint.save().dict())

    def read(self, identifier: str):
        return Complaint(**MongoComplaint.objects.get(id=identifier).dict())

    def update(self, identifier: str, modification_complaint: ModificationComplaint):
        mongo_complaint = MongoComplaint.objects.get(id=identifier)
        mongo_complaint.update(**modification_complaint.dict())
        return self.read(identifier)

    def delete(self, identifier: str):
        MongoComplaint.objects(id=identifier).delete()
        return None


complaint_service = ComplaintService()
