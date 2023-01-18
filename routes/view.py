import json
from extensions import db
from flask import request, jsonify, Blueprint
from models import vending_machine, stock

# bp: blueprint
view_bp = Blueprint("view_bp", __name__)

VendingMachine = vending_machine.VendingMachine
Stock = stock.Stock

def view_all_vending_machines():
    machines = VendingMachine.query.order_by(VendingMachine.id)
    machines_list = []
    for machine in machines:
        machines_list.append({"id": machine.id,
                              "location": machine.location
                              })
    return machines_list


@view_bp.route("/view/<ID>/info", methods=['GET'])
def search_machine_from_id(ID):
    response = VendingMachine.query.get(ID)
    if response is None:
        return jsonify({}), 404
    else:
        return jsonify({"id": response.id,
                        "location": response.location}), 200


@view_bp.route("/view_machine", methods=['GET'])
def view_machines():
    return json.dumps(view_all_vending_machines())


