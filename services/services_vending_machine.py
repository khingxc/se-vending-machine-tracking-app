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

    def create_machine(self, location):
        if location is None:
            return abort(400)
        new_machine = VendingMachine(location=location)
        db.session.add(new_machine)
        db.session.commit()
        return new_machine

    def delete_machine(self, ID):
        machine = VendingMachine.query.get(ID)
        if machine is None:
            return abort(404)
        machine_stocks = Utils.filter_list("stock", ID)
        for machine_stock in machine_stocks:
            db.session.delete(machine_stock)
        db.session.delete(machine)
        db.session.commit()
        return "", 204

    def get_machine(self, ID):
        machine = VendingMachine.query.get(ID)
        if machine is None:
            return abort(404)
        else:
            return jsonify(machine.serializer()), 200

    def get_all_machines(self, ID=None):
        all_machines = Utils.filter_list("machine")
        return json.dumps([m.serializer() for m in all_machines])

    def add_item(self, ID, product, amount):
        if product is None or amount is None:
            return abort(400)
        if ID.isdigit():
            try:
                check_duplicate = Stock.query.filter(Stock.machine_id == ID).filter(Stock.product == product).all()
                if len(check_duplicate) > 0:
                    item = Stock.query.filter(Stock.machine_id == ID).filter(Stock.product == product).first()
                    updated_amount = item.amount + int(amount)
                    item.amount = updated_amount
                    db.session.commit()
                    return jsonify(item.serializer()), 201
                else:
                    new_stock = Stock(machine_id=ID, product=product, amount=amount)
                    db.session.add(new_stock)
                    db.session.commit()
                    return jsonify(new_stock.serializer()), 201
            except:
                return abort(400)
        else:
            return abort(400)
