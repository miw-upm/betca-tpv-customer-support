from typing import Optional

from pydantic import BaseModel, confloat


class Article(BaseModel):
    barcode: str
    description: str
    retailPrice: confloat(ge=0)
    stock: Optional[int]
