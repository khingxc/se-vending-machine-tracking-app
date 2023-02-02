import os
import unittest

from dotenv import load_dotenv
from werkzeug.exceptions import HTTPException

from app import app
from models.model_stock import Stock
from services.services_vending_machine import VendingMachineServices
from services.utils import Utils, random_amount, random_string

load_dotenv()

local_host_address = os.environ["LOCALHOST_ADDR"]
view_all_machine_url = f"{local_host_address}/machine"


class TestAddItem(unittest.TestCase):
    """Test add items to machines with additional cases included +/- cases and testing from functions and APIs."""

    def test_add_item_api_success(self) -> None:
        """Test adding item to existed machine with all requirements via API. Expected Result: Item added."""
        with app.app_context():
            machine_id = Utils().get_valid_machine_id()
            mock_item = random_string()
            mock_amount = random_amount()
            add_item_url = f"{local_host_address}/machine/{machine_id}/add-item"
            response = app.test_client().post(
                add_item_url, data={"product": mock_item, "amount": mock_amount}
            )
            response_json = response.get_json()
            assert response.status_code == 201
            assert response_json["product"] == mock_item
            assert response_json["amount"] == mock_amount

    def test_add_item_api_fail_no_param(self) -> None:
        """Test adding item to existed machine with invalid requirement via API expected error code 400."""
        with app.app_context():
            machine_id = Utils().get_valid_machine_id()
            add_item_url = f"{local_host_address}/machine/{machine_id}/add-item"
            response = app.test_client().post(
                add_item_url, data={"product": "", "amount": 0}
            )
            assert response.status_code == 400

    def test_add_item_api_fail_no_machine(self) -> None:
        """Test adding item to non-existed machine with all requirements via API expected error code 404."""
        with app.app_context():
            random_id = Utils().get_invalid_machine_id()
            mock_item = random_string()
            mock_amount = random_amount()
            add_item_url = f"{local_host_address}/machine/{random_id}/add-item"
            response = app.test_client().post(
                add_item_url, data={"product": mock_item, "amount": mock_amount}
            )
            assert response.status_code == 404

    def test_add_item_func_fail_no_param(self) -> None:
        """Test adding item to existed machine with invalid requirement via function expected error code 400."""
        with self.assertRaises(HTTPException) as http_error:
            with app.app_context():
                machine_id = Utils().get_valid_machine_id()
                VendingMachineServices().add_item(machine_id, "", 0)
                assert http_error.exception.code == 400

    def test_add_item_func_fail_no_machine(self) -> None:
        """Test adding item to non-existed machine with all requirements via function expected error code 404."""
        with self.assertRaises(HTTPException) as http_error:
            with app.app_context():
                mock_item = random_string()
                mock_amount = random_amount()
                random_id = Utils().get_invalid_machine_id()
                VendingMachineServices().add_item(random_id, mock_item, mock_amount)
                assert http_error.exception.code == 404

    def test_add_item_func_successful_add_new_item(self) -> None:
        """Test adding item to existed machine with all requirements via function (new item) expected item added."""
        with app.app_context():
            machine_id: int = Utils().get_valid_machine_id()
            mock_item: str = random_string()
            mock_amount: int = random_amount()
            new_item = VendingMachineServices().add_item(
                machine_id, mock_item, mock_amount
            )
            assert new_item.machine_id == machine_id
            assert new_item.product == mock_item
            assert new_item.amount == mock_amount
            assert type(new_item) == Stock

    def test_add_item_by_function_successful_add_existed_item(self) -> None:
        """Test adding item to existed machine with all requirements via function (existed item) expected item added."""
        with app.app_context():
            machine_id: int = Utils().get_valid_machine_id()
            mock_item: str = random_string()
            mock_amount: int = random_amount()
            VendingMachineServices().add_item(machine_id, mock_item, mock_amount)
            updated_item = VendingMachineServices().add_item(
                machine_id, mock_item, mock_amount
            )
            assert updated_item.machine_id == machine_id
            assert updated_item.product == mock_item
            assert updated_item.amount == mock_amount * 2
            assert type(updated_item) == Stock


if __name__ == "__main__":
    unittest.main()
