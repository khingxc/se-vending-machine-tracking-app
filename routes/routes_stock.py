from services import utils
from flask import request, Blueprint
from models import model_vending_machine, model_stock
from services.services_vending_machine import VendingMachineServices

# bp: blueprint
routes_stock_bp = Blueprint("routes_stock_bp", __name__)

Utils = utils.Utils
VendingMachine = model_vending_machine.VendingMachine
Stock = model_stock.Stock


@routes_stock_bp.route("/machine/<vending_machine_id>/item", methods=["GET"])
def all_items_in_machine(vending_machine_id: int):
    return VendingMachineServices().all_items(vending_machine_id)


@routes_stock_bp.route("/machine/<vending_machine_id>/add_item", methods=["POST"])
def add_item_to_machine(vending_machine_id: int):
    product: str = request.form.get("product")
    amount: str = request.form.get("amount")
    return VendingMachineServices().add_item(machine_id=vending_machine_id, product=product, amount=int(amount))


@routes_stock_bp.route("/machine/<vending_machine_id>/delete_item", methods=["DELETE"])
def delete_item(vending_machine_id: int):
    product: str = request.form.get("product")
    return VendingMachineServices().delete_item(machine_id=vending_machine_id, product=product)


@routes_stock_bp.route("/machine/<vending_machine_id>/edit_item", methods=["POST"])
def edit_item_on_machine(vending_machine_id: int):
    product: str = request.form.get("product")
    amount: str = request.form.get("amount")
    return VendingMachineServices().edit_item(machine_id=vending_machine_id, product=product, amount=int(amount))
