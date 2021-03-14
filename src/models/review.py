from typing import Optional

from pydantic import BaseModel, confloat, conint, constr

from src.models.article import Article
from src.rest_client.core_api import assert_article_existing_and_return


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


def __to_out_review(review, token):
    article = assert_article_existing_and_return(str(token), review.barcode)
    return OutReview(**review.dict(), article=article)
