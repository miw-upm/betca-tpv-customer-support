from datetime import datetime

from fastapi import HTTPException, status

from src.data import complaint_data
from src.models.complaint import Complaint, ModificationComplaint
from src.rest_client.core_api import assert_article_existing


def find(mobile):
    return complaint_data.find_by_mobile(mobile)


def create(customer, modification_complaint: ModificationComplaint):
    assert_article_existing(customer['token'], modification_complaint.barcode)
    complaint = Complaint(**modification_complaint.dict(), mobile=customer['mobile'], registration_date=datetime.now())
    return complaint_data.create(complaint)


def read(mobile, identifier):
    complaint = complaint_data.read(identifier)
    if mobile != complaint.mobile:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions for other customer")
    return complaint


def update(customer, identifier, modification_complaint: ModificationComplaint):
    complaint = read(customer['mobile'], identifier)
    assert_article_existing(customer['token'], modification_complaint.barcode)
    complaint.barcode = modification_complaint.barcode
    complaint.description = modification_complaint.description
    return complaint_data.update(complaint)


def delete(mobile, identifier):
    complaint_data.delete(mobile, identifier)
