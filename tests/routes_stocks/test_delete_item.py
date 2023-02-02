import os
import unittest

from dotenv import load_dotenv
from werkzeug.exceptions import HTTPException

from app import app
from models.model_vending_machine import VendingMachine
from services.services_vending_machine import VendingMachineServices
from services.utils import Utils, random_amount, random_string

load_dotenv()

local_host_address = os.environ["LOCALHOST_ADDR"]


class TestDeleteItem(unittest.TestCase):
    """Test delete items to machines with additional cases included +/- cases and testing from functions and APIs."""

    def test_delete_item_by_api_success(self) -> None:
        """Test deleting item from existed machine via API expected a successful item delete."""
        with app.app_context():
            mock_location = random_string()
            new_machine: VendingMachine = VendingMachineServices().create_machine(
                mock_location
            )
            new_machine_id: int = new_machine.id
            mock_item = random_string()
            mock_amount = random_amount()
            add_item_url = f"{local_host_address}/machine/{new_machine_id}/add-item"
            response_create = app.test_client().post(
                add_item_url, data={"product": mock_item, "amount": mock_amount}
            )
        assert response_create.status_code == 201
        delete_item_url = f"{local_host_address}/machine/{new_machine_id}/delete-item"
        response_delete = app.test_client().delete(
            delete_item_url, data={"product": mock_item}
        )
        assert response_delete.status_code == 204

    def test_delete_item_by_api_fail_no_params(self) -> None:
        """Test deleting item with no input via API expected error code 400 (bad request)."""
        with app.app_context():
            machine_id = Utils().get_valid_machine_id()
            delete_item_url = f"{local_host_address}/machine/{machine_id}/delete-item"
            response_delete = app.test_client().delete(delete_item_url)
        assert response_delete.status_code == 400

    def test_delete_item_by_function_successful(self) -> None:
        """Test deleting item in existed machine via function expected to be successful."""
        with app.app_context():
            machine_id = Utils().get_valid_machine_id()
            mock_item = random_string()
            mock_amount = random_amount()
            add_item_url = f"{local_host_address}/machine/{machine_id}/add-item"
            response_create = app.test_client().post(
                add_item_url, data={"product": mock_item, "amount": mock_amount}
            )
            assert response_create.status_code == 201
            delete_response: tuple[str, int] = VendingMachineServices().delete_item(
                machine_id, mock_item
            )
            delete_response_status_code = delete_response[1]
            assert delete_response_status_code == 204

    def test_delete_item_by_function_fail_invalid_product(self) -> None:
        """Test deleting item with invalid product via function expected error code 400."""
        with self.assertRaises(HTTPException) as http_error:
            with app.app_context():
                machine_id = Utils().get_valid_machine_id()
                VendingMachineServices().delete_item(machine_id, "")
                assert http_error.exception.code == 400

    def test_delete_item_by_function_fail_no_machine(self) -> None:
        """Test deleting item in non-existed machine via function expected error code 404."""
        with self.assertRaises(HTTPException) as http_error:
            with app.app_context():
                random_id = Utils().get_invalid_machine_id()
                mock_item = random_string()
                VendingMachineServices().delete_item(random_id, mock_item)
                assert http_error.exception.code == 404

    def test_delete_item_by_function_fail_item_not_existed(self) -> None:
        """Test deleting invalid item in machine via function expected error code 404."""
        with self.assertRaises(HTTPException) as http_error:
            with app.app_context():
                machine_id = Utils().get_valid_machine_id()
                mock_item = random_string()
                VendingMachineServices().delete_item(machine_id, mock_item)
                assert http_error.exception.code == 404


if __name__ == "__main__":
    unittest.main()
