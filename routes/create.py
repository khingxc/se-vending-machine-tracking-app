from extensions import db
from flask import request, jsonify, Blueprint
from models import vending_machine

# bp: blueprint
create_bp = Blueprint("create_bp", __name__)

VendingMachine = vending_machine.VendingMachine


@create_bp.route("/create_machine", methods=['POST'])
def create_vending_machine():
    location = request.form.get("location")
    print(location)
    if location is None:
        return jsonify(error={"location": "this field is required"}), 400
    new_machine = VendingMachine(location=location)
    db.session.add(new_machine)
    db.session.commit()
    return jsonify({"location": location, "id": new_machine.id}), 201
