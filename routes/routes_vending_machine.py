import json

from flask import Blueprint, jsonify, request

from models import model_stock, model_vending_machine
from services.services_vending_machine import VendingMachineServices

# bp: blueprint
routes_vending_machine_bp = Blueprint("routes_vending_machine", __name__)

VendingMachine = model_vending_machine.VendingMachine
Stock = model_stock.Stock


@routes_vending_machine_bp.route("/machine", methods=["GET"])
def view_all_machines() -> str:
    """View all machines created and return list of machines."""
    all_machines = VendingMachineServices().get_all_machines()
    return json.dumps([m.serializer() for m in all_machines])


@routes_vending_machine_bp.route("/machine/create", methods=["POST"])
def create_vending_machine() -> tuple[str, int]:
    """Create new machine and return the data of the created machine."""
    location: str = request.form.get("location")
    new_machine = VendingMachineServices().create_machine(location)
    return jsonify(new_machine.serializer()), 201


@routes_vending_machine_bp.route("/machine/<vending_machine_id>/info", methods=["GET"])
def view_machine(vending_machine_id: int) -> tuple[str, int]:
    """View existed machine and return its data. Else, error code."""
    result: VendingMachine = VendingMachineServices().get_machine(vending_machine_id)
    view_machine_success: bool = type(result) == VendingMachine
    if view_machine_success:
        return jsonify(result.serializer()), 200
    return result


@routes_vending_machine_bp.route("/machine/<vending_machine_id>/edit", methods=["POST"])
def edit_machine(vending_machine_id: int) -> tuple[str, int]:
    """Update existed machine and return its new updated data. Else, error code."""
    location: str = request.form.get("location")
    result = VendingMachineServices().edit_machine(vending_machine_id, location)
    edit_success: bool = type(result) == VendingMachine
    if edit_success:
        return jsonify(result.serializer()), 200
    return result


@routes_vending_machine_bp.route(
    "/machine/<vending_machine_id>/delete", methods=["DELETE"]
)
def delete_machine(vending_machine_id: int) -> tuple[str, int]:
    """Delete existed machine and return status code 204 to confirm the success. Else, error code."""
    return VendingMachineServices().delete_machine(vending_machine_id)
