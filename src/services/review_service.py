from fastapi import HTTPException, status

from src.models.article import Article
from src.models.review import DBReview, Review, EmptyReview, OutReview
from src.rest_client.core_api import assert_article_existing_and_return

mock_articles = [
    Article(barcode="8400000000017", description="Mock most rated article", retailPrice=30),
    Article(barcode="8400000000024", description="Mock second most rated article", retailPrice=5, stock=15),
    Article(barcode="8400000000031", description="Mock third most rated article", retailPrice=305),
    Article(barcode="8400000000048", description="Nothing", retailPrice=305),
    Article(barcode="8400000000055", description="Another article", retailPrice=305),
    Article(barcode="8400000000079", description="Another of another article", retailPrice=305),
    Article(barcode="8400000000086", description="Look at this article", retailPrice=305)
]

mock_reviews = [
    Review(id="1", barcode=mock_articles[0].barcode, score=2.5, opinion="Is ok but not that much"),
    Review(id="2", barcode=mock_articles[1].barcode, score=5, opinion="Best product"),
    Review(id="3", barcode=mock_articles[2].barcode, score=0.5, opinion="Really bad")
]

mock_out_reviews = [
    OutReview(id="1", article=mock_articles[0], score=2.5, opinion="Is ok but not that much"),
    OutReview(id="2", article=mock_articles[1], score=5, opinion="Best product"),
    OutReview(id="3", article=mock_articles[2], score=0.5, opinion="Really bad"),
    EmptyReview(article=mock_articles[3]),
    EmptyReview(article=mock_articles[4]),
    EmptyReview(article=mock_articles[5]),
    EmptyReview(article=mock_articles[6])
]


def create(customer, review_creation: Review):
    article = assert_article_existing_and_return(customer['token'], review_creation.barcode)
    return OutReview(**review_creation.dict(), article=article)
    # return review_data.create(review_creation)


def read(mobile, identifier):
    # review = review_data.read(identifier)
    # Mock, see if operating with correct dto
    review = None
    for mock_review in mock_reviews:
        if mock_review.id == identifier:
            review = DBReview(**mock_review.dict(), mobile=mobile)

    if mobile != review.mobile:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions for other customer")
    return review


def update(customer, ide, review_updating: Review):
    db_review = read(customer['mobile'], ide)
    article = assert_article_existing_and_return(customer['token'], review_updating.barcode)
    db_review.opinion = review_updating.opinion
    db_review.score = review_updating.score
    return OutReview(**db_review.dict(), article=article)
    # return review_data.update(db_review)


def find(mobile):
    # First, find by mobile the Reviews
    # Second, find all articles that appears on tickets by mobile (query on another API)
    # Third, delete all articles that already appear on Reviews
    # Fourth, create EmptyReviews attaching each article
    # Return collection
    return mock_out_reviews
    # return review_data.find_by_mobile(mobile)


def top_articles():
    # First, recover each article with their reviews (ids)
    # Second, operate and store votes - averageScore
    # Third, sort list by an average of votes-score
    # Return around 3 or 5 articles
    return [mock_articles[0], mock_articles[1], mock_articles[2]]
