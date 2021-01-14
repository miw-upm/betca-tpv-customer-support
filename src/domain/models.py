import datetime

from pydantic import BaseModel, conint, constr


class ModificationComplaint(BaseModel):
    barcode: constr(min_length=4, strip_whitespace=True)
    description: str


class Complaint(ModificationComplaint):
    mobile: conint(gt=1)
    id: str
    registration_date: datetime.datetime
