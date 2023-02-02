import os
import unittest

from dotenv import load_dotenv
from werkzeug.exceptions import HTTPException

from app import app
from services import utils
from services.services_vending_machine import VendingMachineServices
from services.utils import Utils, random_amount, random_string

load_dotenv()

local_host_address = os.environ["LOCALHOST_ADDR"]
view_all_machine_url = f"{local_host_address}/machine"


class TestEditItem(unittest.TestCase):
    """Test edit items to machines with additional cases included +/- cases and testing from functions and APIs."""

    def test_edit_item_by_api_success(self) -> None:
        """Test editing item in existed machine via API expected to be successful with status code 200."""
        mock_item: str = random_string()
        mock_amount = random_amount()
        with app.app_context():
            machine_id = Utils().get_valid_machine_id()
            VendingMachineServices().add_item(machine_id, mock_item, mock_amount)
            edit_item_url = f"{local_host_address}/machine/{machine_id}/edit-item"
            new_amount = mock_amount + 20
            response_edit_item = app.test_client().post(
                edit_item_url, data={"product": mock_item, "amount": new_amount}
            )
            assert response_edit_item.status_code == 200

    def test_edit_item_by_api_fail_no_params(self) -> None:
        """Test editing item with no param on existed machine via API expected to get error code 400."""
        with app.app_context():
            machine_id = Utils().get_valid_machine_id()
            edit_item_url = f"{local_host_address}/machine/{machine_id}/edit-item"
            response_edit_item = app.test_client().post(
                edit_item_url, data={"product": "", "amount": 0}
            )
            assert response_edit_item.status_code == 400

    def test_edit_item_by_api_fail_no_machine(self) -> None:
        """Test editing item on non-existed machine via API expected to get error code 404."""
        with app.app_context():
            random_id = Utils().get_invalid_machine_id()
            mock_item = utils.random_string()
            mock_amount = random_amount()
            edit_item_url = f"{local_host_address}/machine/{random_id}/edit-item"
            response_edit_item = app.test_client().post(
                edit_item_url, data={"product": mock_item, "amount": mock_amount}
            )
            assert response_edit_item.status_code == 404

    def test_edit_item_by_function_success(self) -> None:
        """Test editing item on existed machine via function expected to be successful with status code 200."""
        mock_item: str = random_string()
        mock_amount = random_amount()
        with app.app_context():
            machine_id = Utils().get_valid_machine_id()
            VendingMachineServices().add_item(machine_id, mock_item, mock_amount)
            new_amount = mock_amount + 20
            updated_stock: list = VendingMachineServices().edit_item(
                machine_id, mock_item, new_amount
            )
            stocks_list = [[stock.product, stock.amount] for stock in updated_stock]
            assert [mock_item, new_amount] in stocks_list

    def test_edit_item_by_function_success_remove_item(self) -> None:
        """Test editing item with amount 0 via function expected to have a successful delete the item from machine."""
        mock_item: str = random_string()
        mock_amount = random_amount()
        with app.app_context():
            machine_id = Utils().get_valid_machine_id()
            VendingMachineServices().add_item(machine_id, mock_item, mock_amount)
            updated_stock: list = VendingMachineServices().edit_item(
                machine_id, mock_item, 0
            )
            items_list = [stock.product for stock in updated_stock]
            assert mock_item not in items_list

    def test_edit_item_by_function_success_add_new_item(self) -> None:
        """Test editing item (add new item) to existed machine via function expected new item to be included."""
        mock_item: str = random_string()
        mock_amount = random_amount()
        with app.app_context():
            machine_id = Utils().get_valid_machine_id()
            VendingMachineServices().add_item(machine_id, mock_item, mock_amount)
            new_mock_item: str = random_string()
            new_mock_amount: int = mock_amount + 20
            updated_stock: list = VendingMachineServices().edit_item(
                machine_id, new_mock_item, new_mock_amount
            )
            items_list = [stock.product for stock in updated_stock]
            assert new_mock_item in items_list

    def test_edit_item_by_function_fail_invalid_product(self) -> None:
        """Test editing item (invalid product) from existed machine via function expected error code 400."""
        mock_item: str = random_string()
        mock_amount = random_amount()
        with self.assertRaises(HTTPException) as http_error:
            with app.app_context():
                machine_id = Utils().get_valid_machine_id()
                VendingMachineServices().add_item(machine_id, mock_item, mock_amount)
                VendingMachineServices().edit_item(machine_id, "", 0)
                assert http_error.exception.code == 400

    def test_edit_item_by_function_fail_no_machine(self) -> None:
        """Test editing item on non-existed machine via function expected error code 404."""
        with self.assertRaises(HTTPException) as http_error:
            with app.app_context():
                mock_item: str = random_string()
                mock_amount = random_amount()
                random_id = Utils().get_invalid_machine_id()
                machine_id = Utils().get_valid_machine_id()
                new_amount = mock_amount + 20
                VendingMachineServices().add_item(machine_id, mock_item, mock_amount)
                VendingMachineServices().edit_item(random_id, mock_item, new_amount)
                assert http_error.exception.code == 404


if __name__ == "__main__":
    unittest.main()
