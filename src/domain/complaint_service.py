from datetime import datetime

from fastapi import HTTPException, status

from src.domain.models import Complaint, ModificationComplaint
from src.data import complaint_data
from src.rest_client.core_api import assert_article_existing


def find(mobile):
    return complaint_data.find_by_mobile(mobile)


def create(mobile, modification_complaint: ModificationComplaint):
    assert_article_existing(modification_complaint.barcode)
    complaint = Complaint(**modification_complaint.dict(), mobile=mobile, registration_date=datetime.now())
    return complaint_data.create(complaint)


def read(mobile, identifier):
    complaint = complaint_data.read(identifier)
    if mobile != complaint.mobile:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions for other customer")
    return complaint


def update(mobile, identifier, modification_complaint: ModificationComplaint):
    complaint = read(mobile, identifier)
    assert_article_existing(modification_complaint.barcode)
    complaint.barcode = modification_complaint.barcode
    complaint.description = modification_complaint.description
    return complaint_data.update(complaint)


def delete(mobile, identifier):
    complaint_data.delete(mobile, identifier)
