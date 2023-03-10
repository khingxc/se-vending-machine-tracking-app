import unittest

from werkzeug.exceptions import HTTPException

from app import app
from services.services_vending_machine import VendingMachineServices
from services.utils import Utils, random_amount, random_string
from tests.routes_vending_machine.test_create_machine import TestCreateMachine


class TestDeleteMachine(unittest.TestCase):
    """Test delete machine with additional cases included +/- cases and testing from functions and APIs."""

    def test_delete_machine_by_api_success(self) -> None:
        """Test deleting machine with valid machine id via API expected status code 204."""
        with app.app_context():
            machine_id: int = TestCreateMachine().test_create_machine_by_api_success()
            delete_machine_url = f"/machine/{machine_id}/delete"
            response = app.test_client().delete(delete_machine_url)
            assert response.status_code == 204

    def test_delete_machine_by_api_fail_no_machine(self) -> None:
        """Test deleting machine with invalid machine id via API expected error code 404."""
        with app.app_context():
            random_id = Utils().get_invalid_machine_id()
            delete_machine_url = f"/machine/{random_id}/delete"
            response = app.test_client().delete(delete_machine_url)
            assert response.status_code == 404

    def test_delete_machine_by_function_success(self) -> None:
        """Test deleting machine with valid machine id via function expected status code 204."""
        with app.app_context():
            machine_id: int = TestCreateMachine().test_create_machine_by_api_success()
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
            machine_id: int = TestCreateMachine().test_create_machine_by_api_success()
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
