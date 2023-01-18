from extensions import db
from flask import request, jsonify, Blueprint
from models import vending_machine

# bp: blueprint
delete_bp = Blueprint("delete_bp", __name__)

VendingMachine = vending_machine.VendingMachine


@delete_bp.route("/delete_machine/<ID>", methods=['DELETE'])
def delete_machine(ID):
    response = VendingMachine.query.get(ID)
    if response is None:
        return jsonify({}), 404
    db.session.delete(response)
    db.session.commit()
    return "", 204
