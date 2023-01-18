from extensions import db


class VendingMachine(db.Model):
    __tablename__ = 'vending_machine'
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(length=255))

    def __init__(self, location):
        self.location = location

    def serializer(self):
        return {
            'id': self.id,
            'location': self.location,
        }
