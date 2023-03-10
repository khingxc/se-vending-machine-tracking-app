import json
import unittest

from werkzeug.exceptions import HTTPException

from app import app
from models.model_stock import Stock
from services.services_vending_machine import VendingMachineServices
from services.utils import Utils, random_amount, random_string
from tests.routes_vending_machine.test_create_machine import TestCreateMachine


def create_machine_with_stock() -> tuple[int, str, int]:
    """Create new machine that has an item inside. Return machine ID, product name, and product amount."""
    with app.app_context():
        machine_id: int = TestCreateMachine().test_create_machine_by_api_success()
        mock_item = random_string()
        mock_amount = random_amount()
        add_item_url = f"/machine/{machine_id}/add-item"
        response_create = app.test_client().post(
            add_item_url, data={"product": mock_item, "amount": mock_amount}
        )
        assert response_create.status_code == 201
    return machine_id, mock_item, mock_amount


class TestViewItem(unittest.TestCase):
    """Test view items to machines with additional cases included +/- cases and testing from functions and APIs."""

    def test_view_item_by_api_success(self) -> None:
        """Test viewing item on existed machine via API expected code 200 & matching product and its amount."""
        with app.app_context():
            new_machine_with_stock = create_machine_with_stock()
            machine_id: int = new_machine_with_stock[0]
            mock_item: str = new_machine_with_stock[1]
            mock_amount: int = new_machine_with_stock[2]
            view_item_url = f"/machine/{machine_id}/item"
            response_view_item = app.test_client().get(view_item_url)
            response_view_item_json = (response_view_item.get_data()).decode("utf-8")
            response_in_string = response_view_item_json[
                1 : len(response_view_item_json) - 1
            ]
            response_in_dict = json.loads(response_in_string)
            assert response_view_item.status_code == 200
            assert response_in_dict["product"] == mock_item
            assert response_in_dict["amount"] == mock_amount

    def test_view_item_by_api_fail_no_machine(self) -> None:
        """Test viewing item on non-existed machine via API expected error code 404."""
        with app.app_context():
            random_id = Utils().get_invalid_machine_id()
            view_item_url = f"/machine/{random_id}/item"
            response_view_item = app.test_client().get(view_item_url)
            assert response_view_item.status_code == 404

    def test_view_item_by_function_success(self) -> None:
        """Test viewing item on existed machine via function expected the match results."""
        with app.app_context():
            new_machine_with_stock = create_machine_with_stock()
            machine_id: int = new_machine_with_stock[0]
            mock_item: str = new_machine_with_stock[1]
            mock_amount: int = new_machine_with_stock[2]
            item_in_new_machine: Stock = VendingMachineServices().all_items(machine_id)[
                0
            ]
            saved_item = item_in_new_machine.product
            saved_amount = item_in_new_machine.amount
            assert saved_item == mock_item
            assert saved_amount == mock_amount

    def test_view_item_by_function_fail_no_machine(self) -> None:
        """Test viewing item on non-existed machine via function expected error code 404."""
        with self.assertRaises(HTTPException) as http_error:
            with app.app_context():
                random_id: int = Utils().get_invalid_machine_id()
                VendingMachineServices().all_items(random_id)
                assert http_error.exception.code == 404


if __name__ == "__main__":
    unittest.main()
