from fastapi import HTTPException, status

from src.models.article import Article
from src.models.review import CreationReview, Review, EmptyReview
from src.rest_client.core_api import assert_article_existing

mock_articles = [
    Article(barcode="00000002", description="Mock most rated article", retailPrice=30),
    Article(barcode="00000001", description="Mock second most rated article", retailPrice=5, stock=15),
    Article(barcode="00003201", description="Mock third most rated article", retailPrice=305),
    Article(barcode="00003202", description="Nothing", retailPrice=305),
    Article(barcode="00003203", description="Another article", retailPrice=305),
    Article(barcode="00003204", description="Another of another article", retailPrice=305),
    Article(barcode="00003205", description="Look at this article", retailPrice=305)
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


def create(customer, review_creation: CreationReview):
    assert_article_existing(customer['token'], review_creation.article.barcode)
    return Review(**review_creation.dict())
    # return review_data.create(review_creation)


def read(mobile, identifier):
    # review = review_data.read(identifier)
    # Mock, see if operating with correct dto
    review = None
    for mock_review in [mock_reviews[0], mock_reviews[1], mock_reviews[2]]:
        if mock_review.id == identifier:
            review = mock_review.dict()
            review['mobile'] = mobile

    if mobile != review['mobile']:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions for other customer")
    return review


def update(customer, ide, review_updating: Review):
    review = read(customer['mobile'], ide)
    assert_article_existing(customer['token'], review_updating.article.barcode)
    review['opinion'] = review_updating.opinion
    review['score'] = review_updating.score
    return Review(id=review['id'], article=review_updating.article, score=review['score'], opinion=review['opinion'])
    # return review_data.update(review)


def find(mobile):
    return mock_reviews
    # return review_data.find_by_mobile(mobile)


def top_articles():
    # Some operations needed
    return [mock_articles[0], mock_articles[1], mock_articles[2]]
