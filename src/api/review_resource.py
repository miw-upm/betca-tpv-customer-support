from fastapi import APIRouter, Depends

from src.models.article import Article
from src.models.review import Review, EmptyReview, CreationReview
from src.security import JWTBearer

REVIEWS = "/reviews"
reviews = APIRouter(
    prefix=REVIEWS,
    tags=["Reviews"]
)

mock_articles = [
    Article(barcode="#00000002", description="Mock most rated article", retailPrice=30),
    Article(barcode="#00000001", description="Mock second most rated article", retailPrice=5, stock=15),
    Article(barcode="#00003201", description="Mock third most rated article", retailPrice=305),
    Article(barcode="#00003202", description="Nothing", retailPrice=305),
    Article(barcode="#00003203", description="Another article", retailPrice=305),
    Article(barcode="#00003204", description="Another of another article", retailPrice=305),
    Article(barcode="#00003205", description="Look at this article", retailPrice=305)
]

mock_reviews = [
    Review(id="1", article=mock_articles[0], score=2.5, opinion="Is ok but not that much"),
    Review(id="2", article=mock_articles[1], score=5, opinion="Best product"),
    Review(id="3", article=mock_articles[2], score=0.5, opinion="Really bad"),
    EmptyReview(article=mock_articles[3]),
    EmptyReview(article=mock_articles[4]),
    EmptyReview(article=mock_articles[5]),
    EmptyReview(article=mock_articles[6])
]


@reviews.post("")
def create(review_creation: CreationReview, customer=Depends(JWTBearer(["CUSTOMER"]))) -> Review:
    return Review(**review_creation.dict())
    # return review_service.create(customer, review_creation)


@reviews.put("/{ide}")
def update(ide: str, review_updating: Review, customer=Depends(JWTBearer(["CUSTOMER"]))) -> Review:
    return review_updating
    # return review_service.update(customer, ide, review_updating)


@reviews.get("/search")
def search(customer=Depends(JWTBearer(["CUSTOMER"]))):
    return mock_reviews
    # return review_service.find(customer['mobile'])


@reviews.get("/topArticles")
def top_articles():
    return [mock_articles[0], mock_articles[1], mock_articles[2]]
