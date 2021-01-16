from datetime import datetime

from fastapi import HTTPException, status

from .models import Complaint, ModificationComplaint
from ..data import complaint_data
from ..rest_client.core_api import ArticleApi


def find(mobile):
    return complaint_data.find_by_mobile(mobile)


def create(mobile, modification_complaint: ModificationComplaint):
    ArticleApi.article_existing(modification_complaint.barcode)
    complaint = Complaint(**modification_complaint.dict(), mobile=mobile, registration_date=datetime.now())
    return complaint_data.create(complaint)


def read(mobile, identifier):
    complaint = complaint_data.read(identifier)
    if mobile != complaint.mobile:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions for reading")
    return complaint


def update(mobile, identifier, modification_complaint: ModificationComplaint):
    complaint = read(mobile, identifier)
    complaint.description = modification_complaint.description
    return complaint_data.update(complaint)


def delete(mobile, identifier):
    complaint_data.delete(mobile, identifier)
