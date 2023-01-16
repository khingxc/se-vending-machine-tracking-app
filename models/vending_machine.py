from datetime import datetime
from sqlalchemy import DateTime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class VendingMachine(db.Model):
    __tablename__ = 'vending_machine'
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(length=255))
    created_date = db.Column(DateTime, default=datetime.utcnow)

    def __init__(self, location, created_date):
        self.location = location
        self.created_date = created_date

    def serialize(self):
        return {
            'id': self.id,
            'location': self.location,
            'created_date': self.created_date
        }
