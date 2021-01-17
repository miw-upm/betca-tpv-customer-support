from fastapi import APIRouter, Depends

from src.domain import complaint_service
from src.domain.models import Complaint, ModificationComplaint
from src.security import JWTBearer, SecurityContext

COMPLAINTS = "/complaints"
complaints = APIRouter(
    prefix=COMPLAINTS,
    tags=["Complaints"],
    dependencies=[Depends(JWTBearer(["CUSTOMER"]))]
)


def mobile():
    return int(SecurityContext.customer['mobile'])


@complaints.get("/search")
def search():
    return complaint_service.find(mobile())


@complaints.post("")
def create(complaint_creation: ModificationComplaint) -> Complaint:
    return complaint_service.create(mobile(), complaint_creation)


@complaints.get("/{ide}")
def read(ide: str):
    return complaint_service.read(mobile(), ide)


@complaints.put("/{ide}")
def update(ide: str, complaint_updating: ModificationComplaint) -> Complaint:
    return complaint_service.update(mobile(), ide, complaint_updating)


@complaints.delete("/{ide}")
def delete(ide: str):
    return complaint_service.delete(mobile(), ide)