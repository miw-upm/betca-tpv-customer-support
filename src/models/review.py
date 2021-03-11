from typing import Optional

from pydantic import BaseModel, confloat, conint, constr

from src.models.article import Article


class EmptyReview(BaseModel):
    article: Article


class Review(BaseModel):
    id: Optional[str]
    barcode: constr(strip_whitespace=True)
    score: confloat(gt=0, multiple_of=0.5)
    opinion: Optional[str]


class DBReview(Review):
    mobile: conint(gt=0)
