from typing import Optional

from pydantic import BaseModel, confloat

from src.models.article import Article


class EmptyReview(BaseModel):
    article: Article


class CreationReview(EmptyReview):
    opinion: Optional[str]
    score: confloat(gt=0, multiple_of=0.5)


class Review(CreationReview):
    id: Optional[str]
