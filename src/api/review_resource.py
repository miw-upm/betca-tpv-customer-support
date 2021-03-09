from fastapi import APIRouter, Depends

from src.models.review import Review, EmptyReview, CreationReview
from src.security import JWTBearer

REVIEWS = "/reviews"
reviews = APIRouter(
    prefix=REVIEWS,
    tags=["Reviews"]
)

mock_articles = [
    {'barcode': "#00000002", 'description': "Mock most rated article", 'retailPrice': 30},
    {'barcode': "#00000001", 'description': "Mock second most rated article", 'retailPrice': 5, 'stock': 15},
    {'barcode': "#00003201", 'description': "Mock third most rated article", 'retailPrice': 305},
    {'barcode': "#00003202", 'description': "Nothing", 'retailPrice': 305},
    {'barcode': "#00003203", 'description': "Another article", 'retailPrice': 305},
    {'barcode': "#00003204", 'description': "Another of another article", 'retailPrice': 305},
    {'barcode': "#00003205", 'description': "Look at this article", 'retailPrice': 305}
]

mock_reviews = [
    Review(id="1", articleBarcode="#00000002", score=2.5, opinion="Is ok but not that much"),
    Review(id="2", articleBarcode="#00000001", score=5, opinion="Best product"),
    Review(id="3", articleBarcode="#00003201", score=0.5, opinion="Really bad"),
    EmptyReview(articleBarcode="#00003202"),
    EmptyReview(articleBarcode="#00003203"),
    EmptyReview(articleBarcode="#00003204"),
    EmptyReview(articleBarcode="#00003205")
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


@reviews.get("/exists/{ide}")
def exists(ide: str, customer=Depends(JWTBearer(["CUSTOMER"]))):
    if ide == "1" or ide == "2" or ide == "3":
        return True
    else:
        return False


@reviews.get("/topArticles")
def top_articles():
    return [mock_articles[0], mock_articles[1], mock_articles[2]]
