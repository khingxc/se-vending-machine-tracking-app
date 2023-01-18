from extensions import db


class Stock(db.Model):
    __tablename__ = 'stock'
    stock_id = db.Column(db.Integer, primary_key=True)
    machine_id = db.Column(db.Integer, db.ForeignKey('vending_machine.id'))
    product = db.Column(db.String, nullable=False)
    amount = db.Column(db.Integer, nullable=False)

    def __init__(self, machine_id, product, amount):
        self.machine_id = machine_id
        self.product = product
        self.amount = amount

    def serializer(self):
        return {
            'machine_id': self.machine_id,
            'product': self.product,
            'amount': self.amount
        }
