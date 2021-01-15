import logging
from datetime import datetime

from src.data.documents import MongoComplaint
from .models import Complaint, ModificationComplaint
from ..rest_client.core_api import ArticleApi


class ComplaintService:

    def __init__(self):  # constructor
        logging.info('Creating a ComplaintService')

    def find(self, mobile):
        complaints = []
        for item in MongoComplaint.objects(mobile=mobile):
            complaints.append(Complaint(**item.dict()))
        return complaints

    def create(self, mobile, modification_complaint: ModificationComplaint):
        ArticleApi().article_existing(modification_complaint.barcode)
        mongo_complaint = MongoComplaint(**modification_complaint.dict())
        mongo_complaint.mobile = mobile
        mongo_complaint.registration_date = datetime.now()
        return Complaint(**mongo_complaint.save().dict())

    def read(self, mobile, identifier: str):
        mongo_complaint = MongoComplaint.objects(id=identifier, mobile=mobile).get()
        return Complaint(**mongo_complaint.dict())

    def update(self, mobile, identifier: str, modification_complaint: ModificationComplaint):
        mongo_complaint = MongoComplaint.objects(id=identifier, mobile=mobile).get()
        mongo_complaint.update(**modification_complaint.dict())
        return self.read(mobile, identifier)

    def delete(self, mobile, identifier: str):
        MongoComplaint.objects(id=identifier, mobile=mobile).delete()
        return None


complaint_service = ComplaintService()
