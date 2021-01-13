from fastapi import APIRouter

from src.domain.complaint_service import complaint_service
from src.domain.models import Complaint, ModificationComplaint

router = APIRouter(
    prefix="/complaints",
    tags=["complaints"],
)


@router.get("/search")
def find():
    return complaint_service.find()


@router.post("/")
def create(complaint_creation: ModificationComplaint) -> Complaint:
    return complaint_service.create(complaint_creation)


@router.get("/{ide}")
def read(ide: str):
    return complaint_service.read(ide)


@router.put("/{ide}")
def update(ide: str, complaint_updating: ModificationComplaint) -> Complaint:
    return complaint_service.update(ide, complaint_updating)


@router.delete("/{ide}")
def delete(ide: str):
    return complaint_service.delete(ide)
