import os
import unittest

from dotenv import load_dotenv
from werkzeug.exceptions import HTTPException

from app import app
from services.services_vending_machine import VendingMachine, VendingMachineServices
from services.utils import Utils, random_amount, random_string

load_dotenv()

local_host_address = os.environ["LOCALHOST_ADDR"]
view_all_machine_url = f"{local_host_address}/machine"


class TestDeleteMachine(unittest.TestCase):
    """Test delete machine with additional cases included +/- cases and testing from functions and APIs."""

    def test_delete_machine_by_api_success(self) -> None:
        """Test deleting machine with valid machine id via API expected status code 204."""
        mock_location: str = random_string()
        with app.app_context():
            new_machine: VendingMachine = VendingMachineServices().create_machine(
                mock_location
            )
            new_machine_id: int = new_machine.serializer()["id"]
            delete_machine_url = f"{local_host_address}/machine/{new_machine_id}/delete"
            response = app.test_client().delete(delete_machine_url)
            assert response.status_code == 204

    def test_delete_machine_by_api_fail_no_machine(self) -> None:
        """Test deleting machine with invalid machine id via API expected error code 404."""
        with app.app_context():
            random_id = Utils().get_invalid_machine_id()
            delete_machine_url = f"{local_host_address}/machine/{random_id}/delete"
            response = app.test_client().delete(delete_machine_url)
            assert response.status_code == 404

    def test_delete_machine_by_function_success(self) -> None:
        """Test deleting machine with valid machine id via function expected status code 204."""
        with app.app_context():
            machine_id = Utils().get_valid_machine_id()
            delete_machine: tuple[str, int] = VendingMachineServices().delete_machine(
                machine_id
            )
            status_code: int = delete_machine[1]
            assert status_code == 204

    def test_delete_machine_by_function_success_with_stocks(self) -> None:
        """Test deleting existed machine that has item inside via function expected status code 204."""
        mock_item: str = random_string()
        mock_amount = random_amount()
        with app.app_context():
            machine_id = Utils().get_valid_machine_id()
            VendingMachineServices().add_item(machine_id, mock_item, mock_amount)
            delete_machine_response: tuple[
                str, int
            ] = VendingMachineServices().delete_machine(machine_id)
            status_code: int = delete_machine_response[1]
            assert status_code == 204

    def test_delete_machine_by_function_fail(self) -> None:
        """Test deleting machine with invalid id via function expected error code 404."""
        with self.assertRaises(HTTPException) as http_error:
            with app.app_context():
                random_id = Utils().get_invalid_machine_id()
                VendingMachineServices().delete_machine(random_id)
                assert http_error.exception.code == 404


if __name__ == "__main__":
    unittest.main()
