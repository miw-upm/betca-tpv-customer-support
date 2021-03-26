from typing import Optional

from pydantic import BaseModel, confloat, conint, constr

from src.models.article import Article


class EmptyReview(BaseModel):
    article: Article


class BaseReview(BaseModel):
    id: Optional[str]
    score: confloat(gt=0, multiple_of=0.5)
    opinion: Optional[str]


class Review(BaseReview):
    barcode: constr(strip_whitespace=True)


class OutReview(BaseReview):
    article: Article


class DBReview(Review):
    mobile: conint(gt=0)
