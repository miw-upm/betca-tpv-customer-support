import datetime
from typing import Optional

from pydantic import BaseModel, conint, constr


class ModificationComplaint(BaseModel):
    barcode: constr(min_length=4, strip_whitespace=True)
    description: str


class Complaint(ModificationComplaint):
    id: Optional[str]
    mobile: conint(gt=1)
    registration_date: datetime.datetime
