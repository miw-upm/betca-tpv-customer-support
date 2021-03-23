from datetime import datetime
from typing import Optional

from pydantic import BaseModel, conint, constr


class ModificationComplaint(BaseModel):
    barcode: constr(min_length=4, strip_whitespace=True)
    description: str
    opened: bool
    reply: Optional[str]


class Complaint(ModificationComplaint):
    id: Optional[str]
    mobile: conint(ge=0)
    registration_date: datetime

