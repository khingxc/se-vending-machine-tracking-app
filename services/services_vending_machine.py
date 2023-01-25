import json
from flask import abort, jsonify
from extensions import db
from services.utils import Utils
from models import model_vending_machine, model_stock

VendingMachine = model_vending_machine.VendingMachine
Stock = model_stock.Stock


class VendingMachineServices:
    def __init__(self):
        self.db = db

    def create_machine(self, location: str):
        if location is None:
            return abort(400)
        new_machine = VendingMachine(location=location)
        db.session.add(new_machine)
        db.session.commit()
        return new_machine

    def delete_machine(self, machine_id: int):
        machine = VendingMachine.query.get(machine_id)
        if machine is None:
            return abort(404)
        machine_stocks = Utils().filter_list("stock", machine_id)
        for machine_stock in machine_stocks:
            db.session.delete(machine_stock)
        db.session.delete(machine)
        db.session.commit()
        return "", 204

    def edit_machine(self, machine_id: int, location: str):
        machine = VendingMachine.query.get(machine_id)
        if location is None or len(location.strip()) == 0:
            return abort(400)
        if machine is not None:
            machine.location = location
            db.session.commit()
            return jsonify(machine.serializer()), 200
        else:
            return abort(404)

    def get_machine(self, machine_id: int):
        machine = VendingMachine.query.get(machine_id)
        if machine is None:
            return abort(404)
        else:
            return jsonify(machine.serializer()), 200

    def get_all_machines(self):
        all_machines = Utils().filter_list("machine")
        return json.dumps([m.serializer() for m in all_machines])

    def add_item(self, machine_id: int, product: str, amount: int):
        machine = VendingMachine.query.get(machine_id)
        if product is None or amount == 0:
            return abort(400)
        elif machine is None:
            return abort(404)
        else:
            try:
                check_duplicate = (
                    Stock.query.filter(Stock.machine_id == machine_id)
                    .filter(Stock.product == product)
                    .all()
                )
                if len(check_duplicate) > 0:
                    item = (
                        Stock.query.filter(Stock.machine_id == machine_id)
                        .filter(Stock.product == product)
                        .first()
                    )
                    updated_amount = item.amount + int(amount)
                    item.amount = updated_amount
                    db.session.commit()
                    return jsonify(item.serializer()), 201
                else:
                    new_stock = Stock(machine_id=machine_id, product=product, amount=amount)
                    db.session.add(new_stock)
                    db.session.commit()
                    return jsonify(new_stock.serializer()), 201
            except:
                return abort(400)

    def delete_item(self, machine_id: int, product: str):
        machine = VendingMachine.query.get(machine_id)
        target_item = (
            Stock.query.filter(Stock.machine_id == machine_id)
            .filter(Stock.product == product)
            .first()
        )
        if product is None:
            return abort(400)
        elif machine is None or target_item is None:
            return abort(404)
        del_item = (
            Stock.query.filter(Stock.machine_id == machine_id)
            .filter(Stock.product == product)
            .first()
        )
        db.session.delete(del_item)
        db.session.commit()
        return "", 204

    def all_items(self, machine_id: int):
        machine = VendingMachine.query.get(machine_id)
        if machine is None:
            return abort(404)
        items = Utils().filter_list("stock", machine_id)
        return json.dumps([i.serializer() for i in items])

    def edit_item(self, machine_id: int, product: str, amount: int):
        machine = VendingMachine.query.get(machine_id)
        if product is None or len(product.strip()) == 0:
            return abort(400)
        elif machine is None:
            return abort(404)
        if int(amount) == 0:
            self.delete_item(machine_id, product)
        else:
            check_duplicate = (
                Stock.query.filter(Stock.machine_id == machine_id)
                .filter(Stock.product == product)
                .all()
            )
            if len(check_duplicate) > 0:
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
