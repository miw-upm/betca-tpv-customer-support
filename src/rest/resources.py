from fastapi import APIRouter, Depends

from src.domain.complaint_service import complaint_service
from src.domain.models import Complaint, ModificationComplaint
from src.rest.security import JWTBearer

customer = JWTBearer(["CUSTOMER"])

complaints = APIRouter(
    prefix="/complaints",
    tags=["complaints"],
    dependencies=[Depends(customer)]
)


@complaints.get("/search")
def find():
    return complaint_service.find(customer.customer['mobile'])


@complaints.post("")
def create(complaint_creation: ModificationComplaint) -> Complaint:
    return complaint_service.create(customer.customer['mobile'], complaint_creation)


@complaints.get("/{ide}")
def read(ide: str):
    return complaint_service.read(customer.customer['mobile'], ide)


@complaints.put("/{ide}")
def update(ide: str, complaint_updating: ModificationComplaint) -> Complaint:
    return complaint_service.update(customer.customer['mobile'], ide, complaint_updating)


@complaints.delete("/{ide}")
def delete(ide: str):
    return complaint_service.delete(customer.customer['mobile'], ide)
