from mongoengine import Document, StringField, DateTimeField, IntField


class MongoComplaint(Document):
    mobile = IntField(required=True)
    barcode = StringField(required=True)
    description = StringField(required=True)
    registration_date = DateTimeField()

    def __repr__(self):
        return str(self.dict())

    def dict(self):
        return {'id': str(self.id), 'mobile': self.mobile, 'barcode': self.barcode, 'description': self.description,
                'registration_date': self.registration_date}
