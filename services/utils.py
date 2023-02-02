import secrets
import string
from typing import Any, List

from extensions import db
from models import model_stock, model_vending_machine

VendingMachine = model_vending_machine.VendingMachine
Stock = model_stock.Stock


def random_string() -> str:
    """Random a string with length of 10. Mainly use for testing."""
    alphabet = string.ascii_lowercase + string.digits
    return "".join(secrets.choice(alphabet) for _ in range(10))


def random_amount() -> int:
    """Random number of items for testing."""
    return secrets.randbelow(50) + 1


class Utils:
    """Store functions that can be used in many sections."""

    def __init__(self):
        """INIT."""
        self.db = db

    def filter_list(self, data: str, machine_id: int = 0) -> List[Any]:
        """Return list in choices: Machine or Stock of existed Machine. Else, empty list."""
        if data.lower() == "machines":
            machines = VendingMachine.query.order_by(VendingMachine.id)
            return [m for m in machines]
        elif data.lower() == "stock":
            stocks = Stock.query.filter(Stock.machine_id == int(machine_id))
            if stocks is not None:
                return [s for s in stocks]
        else:
            return []

    def get_all_machines(self) -> List[VendingMachine]:
        """Return list of all created machines."""
        return self.filter_list("machines")

    def get_valid_machine_id(self) -> int:
        """Return valid machine id for testing. If DB has no data, create new one."""
        all_machines: list = self.get_all_machines()
        if len(all_machines) > 0:
            all_machines: list = self.get_all_machines()
            random_machine: VendingMachine = secrets.choice(all_machines)
            machine_id: int = random_machine.id
            return machine_id
        return 0

    def get_invalid_machine_id(self) -> int:
        """Return invalid machine id."""
        all_machines: list = self.get_all_machines()
        all_valid_ids: List[int] = [machine.id for machine in all_machines]
        if len(all_valid_ids) == 0:
            return 0
        invalid_id = max(all_valid_ids) * 2
        return invalid_id
