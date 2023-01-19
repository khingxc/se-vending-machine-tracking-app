from services import utils
from flask import request, Blueprint
from models import model_vending_machine, model_stock
from services.services_vending_machine import VendingMachineServices

# bp: blueprint
routes_stock_bp = Blueprint("routes_stock_bp", __name__)

Utils = utils.Utils
VendingMachine = model_vending_machine.VendingMachine
Stock = model_stock.Stock


@routes_stock_bp.route("/machine/<ID>/item", methods=["GET"])
def all_items_in_machine(ID):
    product = request.form.get("product")
    return VendingMachineServices().all_items(ID, product)


@routes_stock_bp.route("/machine/<ID>/add_item", methods=["POST"])
def add_item_to_machine(ID):
    product = request.form.get("product")
    amount = request.form.get("amount")
    return VendingMachineServices().add_item(ID=ID, product=product, amount=amount)


@routes_stock_bp.route("/machine/<ID>/delete_item", methods=["DELETE"])
def delete_item(ID):
    product = request.form.get("product")
    return VendingMachineServices().delete_item(ID=ID, product=product)


@routes_stock_bp.route("/machine/<ID>/edit_item", methods=["POST"])
def edit_item_on_machine(ID):
    product = request.form.get("product")
    amount = request.form.get("amount")
    return VendingMachineServices().edit_item(ID=ID, product=product, amount=amount)
