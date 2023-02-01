"""Initialize Stock Model."""
from typing import TypedDict

from extensions import db


class Stock(db.Model):
    """Stock class to create new stock for storing in vending machines."""

    __tablename__ = "stock"
    stock_id: int = db.Column(db.Integer, primary_key=True)
    machine_id: int = db.Column(db.Integer, db.ForeignKey("vending_machine.id"))
    product: str = db.Column(db.String, nullable=False)
    amount: int = db.Column(db.Integer, nullable=False)

    def __init__(self, machine_id: int, product: str, amount: int) -> None:
        """Initialize stock vars."""
        self.machine_id = machine_id
        self.product = product
        self.amount = amount

    class StockJson(TypedDict):
        """Class of stock serializer."""

        machine_id: int
        product: str
        amount: int

    def serializer(self) -> StockJson:
        """Stock json."""
        return {
            "machine_id": self.machine_id,
            "product": self.product,
            "amount": self.amount,
        }
