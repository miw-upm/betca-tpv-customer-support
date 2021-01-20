from fastapi import APIRouter, Depends

from src.models.complaint import Complaint, ModificationComplaint
from src.security import JWTBearer
from src.services import complaint_service

COMPLAINTS = "/complaints"
complaints = APIRouter(
    prefix=COMPLAINTS,
    tags=["Complaints"],
)


@complaints.get("/search")
def search(customer=Depends(JWTBearer(["CUSTOMER"]))):
    return complaint_service.find(customer['mobile'])


@complaints.post("")
def create(complaint_creation: ModificationComplaint, customer=Depends(JWTBearer(["CUSTOMER"]))) -> Complaint:
    return complaint_service.create(customer, complaint_creation)


@complaints.get("/{ide}")
def read(ide: str, customer=Depends(JWTBearer(["CUSTOMER"]))):
    return complaint_service.read(customer['mobile'], ide)


@complaints.put("/{ide}")
def update(ide: str, complaint_updating: ModificationComplaint, customer=Depends(JWTBearer(["CUSTOMER"]))) -> Complaint:
    return complaint_service.update(customer, ide, complaint_updating)


@complaints.delete("/{ide}")
def delete(ide: str, customer=Depends(JWTBearer(["CUSTOMER"]))):
    return complaint_service.delete(customer['mobile'], ide)
