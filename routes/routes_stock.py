import json
from typing import Any

from flask import Blueprint, jsonify, request

from models import model_stock, model_vending_machine
from services import utils
from services.services_vending_machine import VendingMachineServices

# bp: blueprint
routes_stock_bp = Blueprint("routes_stock_bp", __name__)

Utils = utils.Utils
VendingMachine = model_vending_machine.VendingMachine
Stock = model_stock.Stock


@routes_stock_bp.route("/machine/<vending_machine_id>/item", methods=["GET"])
def all_items_in_machine(vending_machine_id: int) -> str:
    """List all items placed in selected existed machine."""
    items = VendingMachineServices().all_items(vending_machine_id)
    return json.dumps([i.serializer() for i in items])


@routes_stock_bp.route("/machine/<vending_machine_id>/add-item", methods=["POST"])
def add_item_to_machine(vending_machine_id: int) -> tuple[Any, int]:
    """Add item to a vending machine and return list of all items in a machine after updating."""
    product: str = request.form.get("product")
    amount: str = request.form.get("amount")
    result = VendingMachineServices().add_item(
        machine_id=vending_machine_id, product=product, amount=int(amount)
    )
    add_item_success: bool = type(result) == Stock
    if add_item_success:
        return jsonify(result.serializer()), 201
    return result


@routes_stock_bp.route("/machine/<vending_machine_id>/delete-item", methods=["DELETE"])
def delete_item(vending_machine_id: int) -> tuple[str, int]:
    """Delete existed item in machine, and return status code to ensure the success of the process."""
    product: str = request.form.get("product")
    return VendingMachineServices().delete_item(
        machine_id=vending_machine_id, product=product
    )


@routes_stock_bp.route("/machine/<vending_machine_id>/edit-item", methods=["POST"])
def edit_item_on_machine(vending_machine_id: int) -> tuple[Any, int]:
    """Edit item in vending machine, and return all items in machine."""
    product: str = request.form.get("product")
    amount: str = request.form.get("amount")
    result = VendingMachineServices().edit_item(
        machine_id=vending_machine_id, product=product, amount=int(amount)
    )
    if type(result) == list:
        items = VendingMachineServices().all_items(vending_machine_id)
        return json.dumps([i.serializer() for i in items]), 200
    return result
