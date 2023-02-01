from typing import TypedDict

from extensions import db


class VendingMachine(db.Model):
    """Vending machine class to create new machine."""

    __tablename__ = "vending_machine"
    id: int = db.Column(db.Integer, primary_key=True)
    location: str = db.Column(db.String(length=255))

    def __init__(self, location: str):
        """Initialize machine var."""
        self.location: str = location

    class MachineJson(TypedDict):
        """Class of vending machine serializer."""

        id: int
        location: str

    def serializer(self) -> MachineJson:
        """Machine json."""
        return {
            "id": self.id,
            "location": self.location,
        }
