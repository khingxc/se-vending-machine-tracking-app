import json
from flask import request, jsonify, Blueprint
from models import vending_machine

view_bp = Blueprint("view_bp", __name__)

VendingMachine = vending_machine.VendingMachine


def view_all_vending_machines():
    machines = VendingMachine.query.order_by(VendingMachine.created_date.desc())
    machines_list = []
    for machine in machines:
        machines_list.append({"id": machine.id,
                              "location": machine.location,
                              "created_date": str(machine.created_date)})
    return machines_list


@view_bp.route("/view_machine/<ID>", methods=['GET'])
def search_machine_from_id(ID):
    response = VendingMachine.query.get(ID)
    if response is None:
        return jsonify({}), 404
    else:
        return jsonify({"id": response.id,
                        "location": response.location,
                        "created_date": str(response.created_date)}), 200


@view_bp.route("/view_machine", methods=['POST'])
def view_machines():
    return json.dumps(view_all_vending_machines())
