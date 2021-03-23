from datetime import datetime

from fastapi import HTTPException, status

from src.data import complaint_data
from src.models.complaint import Complaint, ModificationComplaint
from src.rest_client.core_api import assert_article_existing_and_return


def find(mobile):
    return complaint_data.find_by_mobile(mobile)


def find_all(role):
    if role != "CUSTOMER":
        return complaint_data.find()


def find_opened(role):
    if role != "CUSTOMER":
        return complaint_data.find_opened()


def create(customer, modification_complaint: ModificationComplaint):
    assert_article_existing_and_return(customer['token'], modification_complaint.barcode)
    complaint = Complaint(**modification_complaint.dict(), mobile=customer['mobile'],
                          registration_date=datetime.now(), opened=True)
    return complaint_data.create(complaint)


def read(mobile, role, identifier):
    complaint = complaint_data.read(identifier)
    if role == 'ADMIN':
        return complaint
    elif role == 'CUSTOMER':
        if mobile != complaint.mobile:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="Not enough permissions for other customer")
        return complaint
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions for read complaints")


def update(user, identifier, modification_complaint: ModificationComplaint):
    complaint = read(user['mobile'], user['role'], identifier)
    assert_article_existing_and_return(user['token'], modification_complaint.barcode)
    if user['role'] == 'ADMIN':
        complaint.opened = False
        complaint.reply = modification_complaint.reply
    elif user['role'] == 'CUSTOMER':
        complaint.barcode = modification_complaint.barcode
        complaint.description = modification_complaint.description
    return complaint_data.update(complaint)


def delete(mobile, identifier):
    complaint_data.delete(mobile, identifier)
