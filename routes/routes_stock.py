from flask import request, Blueprint
from models import model_vending_machine, model_stock
from services.services_vending_machine import VendingMachineServices

# bp: blueprint
routes_stock_bp = Blueprint("routes_stock_bp", __name__)

VendingMachine = model_vending_machine.VendingMachine
Stock = model_stock.Stock


@routes_stock_bp.route("/machine/<ID>/add_item", methods=['POST'])
def add_item_to_machine(ID):
    product = request.form.get("product")
    amount = request.form.get("amount")
    return VendingMachineServices().add_item(ID=ID, product=product, amount=amount)
