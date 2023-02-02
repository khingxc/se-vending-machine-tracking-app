from typing import List

from flask import abort

from extensions import db
from models import model_stock, model_vending_machine
from services.utils import Utils

VendingMachine = model_vending_machine.VendingMachine
Stock = model_stock.Stock


def check_item_existed_in_machine(machine_id: int, product: str) -> bool:
    """Check if the given product is already existed in the machine or not."""
    find_product_in_machine = (
        Stock.query.filter(Stock.machine_id == machine_id)
        .filter(Stock.product == product)
        .all()
    )
    return len(find_product_in_machine) > 0


class VendingMachineServices:
    """Class of all services related to machine."""

    def __init__(self):
        """INIT."""
        self.db = db

    def create_machine(self, location: str) -> VendingMachine:
        """Create new vending machine."""
        if location is None or len(location.strip()) == 0:
            return abort(400)
        new_machine = VendingMachine(location=location)
        db.session.add(new_machine)
        db.session.commit()
        return new_machine

    def delete_machine(self, machine_id: int) -> tuple[str, int]:
        """Delete existed vending machine."""
        machine = VendingMachine.query.get(machine_id)
        if machine is None:
            return abort(404)
        machine_stocks = Utils().filter_list("stock", machine_id)
        for machine_stock in machine_stocks:
            db.session.delete(machine_stock)
        db.session.delete(machine)
        db.session.commit()
        return "", 204

    def edit_machine(self, machine_id: int, location: str) -> VendingMachine:
        """Edit existed machine's info."""
        if location is None or len(location.strip()) == 0:
            return abort(400)
        machine: VendingMachine = VendingMachine.query.get(machine_id)
        if machine is None:
            return abort(404)
        else:
            machine.location = location
            db.session.commit()
            return machine

    def get_machine(self, machine_id: int) -> VendingMachine:
        """Retrieve existed machine by its ID."""
        machine = VendingMachine.query.get(machine_id)
        if machine is None:
            return abort(404)
        return machine

    def get_all_machines(self) -> List[VendingMachine]:
        """Retrieve all created machines."""
        all_machines = Utils().filter_list("machines")
        return all_machines

    def add_existed_product_to_machine(
        self, machine_id: int, product: str, amount: int
    ) -> Stock:
        """Add existed product to the machine and return the updated product info."""
        item: Stock = (
            Stock.query.filter(Stock.machine_id == machine_id)
            .filter(Stock.product == product)
            .first()
        )
        updated_amount: int = item.amount + int(amount)
        item.amount = updated_amount
        db.session.commit()
        return item

    def add_new_item_to_machine(
        self, machine_id: int, product: str, amount: int
    ) -> Stock:
        """Add new product to the existed machine and return the info after updating the machine."""
        new_stock: Stock = Stock(machine_id=machine_id, product=product, amount=amount)
        db.session.add(new_stock)
        db.session.commit()
        return new_stock

    def add_item(
        self, machine_id: int, product: str, amount: int
    ) -> Stock | tuple[str, int]:
        """Add item to the existed machine, and if successful, return info of added item. Else, error code."""
        machine = VendingMachine.query.get(machine_id)
        if product is None or amount == 0 or len(product.strip()) == 0:
            return abort(400)
        elif machine is None:
            return abort(404)
        else:
            item_in_machine = check_item_existed_in_machine(machine_id, product)
            if item_in_machine:
                item: Stock = self.add_existed_product_to_machine(
                    machine_id, product, amount
                )
                return item
            else:
                new_stock: Stock = self.add_new_item_to_machine(
                    machine_id, product, amount
                )
                return new_stock

    def delete_item(self, machine_id: int, product: str) -> tuple[str, int]:
        """Delete existed item in existed machine, and return 204 if successful. Else, error code."""
        machine = VendingMachine.query.get(machine_id)
        if machine is None:
            return abort(404)
        if product is None or len(product.strip()) == 0:
            return abort(400)
        target_item = (
            Stock.query.filter(Stock.machine_id == machine_id)
            .filter(Stock.product == product)
            .first()
        )
        if target_item is None:
            return abort(404)
        del_item = (
            Stock.query.filter(Stock.machine_id == machine_id)
            .filter(Stock.product == product)
            .first()
        )
        db.session.delete(del_item)
        db.session.commit()
        return "", 204

    def all_items(self, machine_id: int) -> List[Stock]:
        """Retrieve list of products in existed machine. Else, error code."""
        machine = VendingMachine.query.get(machine_id)
        if machine is None:
            return abort(404)
        items = Utils().filter_list("stock", machine_id)
        return items

    def edit_item(
        self, machine_id: int, product: str, amount: int
    ) -> List[Stock] | tuple[str, int]:
        """Edit item in existed machine and return updated stock list. Else, error code."""
        machine = VendingMachine.query.get(machine_id)
        if product is None or len(product.strip()) == 0:
            return abort(400)
        elif machine is None:
            return abort(404)
        if int(amount) == 0:
            self.delete_item(machine_id, product)
        else:
            item_in_machine = check_item_existed_in_machine(machine_id, product)
            if item_in_machine:
                item = (
                    Stock.query.filter(Stock.machine_id == machine_id)
                    .filter(Stock.product == product)
                    .first()
                )
                item.amount = amount
                db.session.commit()
            else:
                self.add_item(machine_id, product, amount)
        return self.all_items(machine_id)
