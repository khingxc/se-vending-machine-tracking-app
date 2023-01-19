from extensions import db
from models import model_vending_machine, model_stock

VendingMachine = model_vending_machine.VendingMachine
Stock = model_stock.Stock


class Utils:

    def __init__(self):
        self.db = db

    def filter_list(data, machine_id=0):
        match data.lower():
            case "machine":
                machines = VendingMachine.query.order_by(VendingMachine.id)
                return [m for m in machines]
            case "stock":
                stocks = Stock.query.filter(Stock.machine_id == int(machine_id))
                if stocks is not None:
                    return [s for s in stocks]
        return []
