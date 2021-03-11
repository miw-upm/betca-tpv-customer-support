from fastapi import APIRouter, Depends

from src.models.review import Review, OutReview
from src.security import JWTBearer
from src.services import review_service

REVIEWS = "/reviews"
reviews = APIRouter(
    prefix=REVIEWS,
    tags=["Reviews"]
)


@reviews.post("")
def create(review_creation: Review, customer=Depends(JWTBearer(["CUSTOMER"]))) -> OutReview:
    return review_service.create(customer, review_creation)


@reviews.put("/{ide}")
def update(ide: str, review_updating: Review, customer=Depends(JWTBearer(["CUSTOMER"]))) -> OutReview:
    return review_service.update(customer, ide, review_updating)


@reviews.get("/search")
def search(customer=Depends(JWTBearer(["CUSTOMER"]))):
    return review_service.find(customer['mobile'])


@reviews.get("/topArticles")
def top_articles():
    return review_service.top_articles()
