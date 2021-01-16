from fastapi import APIRouter, Depends

from src.domain import complaint_service
from src.domain.models import Complaint, ModificationComplaint
from src.security import JWTBearer, SecurityContext

COMPLAINTS = "/complaints"
complaints = APIRouter(
    prefix=COMPLAINTS,
    tags=["complaints"],
    dependencies=[Depends(JWTBearer(["CUSTOMER"]))]
)


@complaints.get("/search")
def search():
    return complaint_service.find(SecurityContext.customer['mobile'])


@complaints.post("")
def post(complaint_creation: ModificationComplaint) -> Complaint:
    return complaint_service.create(SecurityContext.customer['mobile'], complaint_creation)


@complaints.get("/{ide}")
def get(ide: str):
    return complaint_service.read(SecurityContext.customer['mobile'], ide)


@complaints.put("/{ide}")
def put(ide: str, complaint_updating: ModificationComplaint) -> Complaint:
    return complaint_service.update(SecurityContext.customer['mobile'], ide, complaint_updating)


@complaints.delete("/{ide}")
def delete(ide: str):
    return complaint_service.delete(SecurityContext.customer['mobile'], ide)
