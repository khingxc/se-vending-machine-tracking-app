from flask import request, jsonify, Blueprint
from models import model_vending_machine, model_stock
from services.services_vending_machine import VendingMachineServices

# bp: blueprint
routes_vending_machine_bp = Blueprint("routes_vending_machine", __name__)

VendingMachine = model_vending_machine.VendingMachine
Stock = model_stock.Stock


@routes_vending_machine_bp.route("/machine", methods=["GET"])
def view_all_machines():
    return VendingMachineServices().get_all_machines()


@routes_vending_machine_bp.route("/machine/create", methods=["POST"])
def create_vending_machine():
    location: str = request.form.get("location")
    new_machine = VendingMachineServices().create_machine(location)
    return jsonify(new_machine.serializer()), 201


@routes_vending_machine_bp.route("/machine/<vending_machine_id>/info", methods=["GET"])
def view_machine(vending_machine_id: int):
    return VendingMachineServices().get_machine(vending_machine_id)


@routes_vending_machine_bp.route("/machine/<vending_machine_id>/edit", methods=["POST"])
def edit_machine(vending_machine_id: int):
    location: str = request.form.get("location")
    return VendingMachineServices().edit_machine(vending_machine_id, location)


@routes_vending_machine_bp.route(
    "/machine/<vending_machine_id>/delete", methods=["DELETE"]
)
def delete_machine(vending_machine_id: int):
    return VendingMachineServices().delete_machine(vending_machine_id)
