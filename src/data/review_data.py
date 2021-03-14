from mongoengine import Document, IntField, StringField, FloatField


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
