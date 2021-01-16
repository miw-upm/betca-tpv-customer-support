from fastapi import HTTPException, status
from mongoengine import Document, StringField, DateTimeField, IntField, DoesNotExist

from src.domain.models import Complaint


class ComplaintDocument(Document):
    mobile = IntField(required=True)
    barcode = StringField(required=True)
    description = StringField(required=True)
    registration_date = DateTimeField()

    def __repr__(self):
        return str(self.dict())

    def dict(self):
        return {'id': str(self.id), 'mobile': self.mobile, 'barcode': self.barcode, 'description': self.description,
                'registration_date': self.registration_date}


def find_by_mobile(mobile) -> [Complaint]:
    complaints = []
    for item in ComplaintDocument.objects(mobile=mobile):
        complaints.append(Complaint(**item.dict()))
    return complaints


def create(complaint) -> Complaint:
    complaint_document = ComplaintDocument(**complaint.dict())
    complaint_document.save()
    return Complaint(**complaint_document.dict())


def read(identifier) -> Complaint:
    try:
        complaint_document = ComplaintDocument.objects(id=identifier).get()
    except DoesNotExist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found Complaint: " + identifier)
    return Complaint(**complaint_document.dict())


def update(complaint) -> Complaint:
    complaint_document = ComplaintDocument.objects(id=complaint.id).get()
    complaint_document.update(**complaint.dict())
    return read(complaint.id)


def delete(mobile, identifier):
    ComplaintDocument.objects(id=identifier, mobile=mobile).delete()
