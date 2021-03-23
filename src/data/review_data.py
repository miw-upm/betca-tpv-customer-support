from fastapi import HTTPException, status
from mongoengine import Document, IntField, StringField, FloatField, DoesNotExist

from src.models.review import Review, DBReview


class ReviewDocument(Document):
    mobile = IntField(required=True)
    barcode = StringField(required=True)
    score = FloatField(required=True)
    opinion = StringField()

    def __repr__(self):
        return str(self.dict())

    def dict(self):
        return {'id': str(self.id), 'mobile': self.mobile, 'barcode': self.barcode, 'score': str(self.score),
                'opinion': self.opinion}


def create(db_review) -> Review:
    review_document = ReviewDocument(**db_review.dict())
    review_document.save()
    return Review(**review_document.dict())


def __read_assured(identifier):
    try:
        return ReviewDocument.objects(id=identifier).get()
    except DoesNotExist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found Review: " + identifier)


def read(identifier) -> DBReview:
    review_document = __read_assured(identifier)
    return DBReview(**review_document.dict())


def update(review) -> Review:
    review_document = __read_assured(review.id)
    review_document.update(**review.dict())
    updated_review = read(review_document.id)
    return Review(**updated_review.dict())


def find_by_mobile(mobile) -> [Review]:
    reviews = []
    for item in ReviewDocument.objects(mobile=mobile):
        reviews.append(Review(**item.dict()))
    return reviews


def find_all() -> [DBReview]:
    reviews = []
    for item in ReviewDocument.objects():
        reviews.append(DBReview(**item.dict()))
    return reviews
