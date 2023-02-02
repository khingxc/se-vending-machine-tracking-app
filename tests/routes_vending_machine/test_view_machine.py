import unittest
from typing import List

from werkzeug.exceptions import HTTPException

from app import app
from models.model_vending_machine import VendingMachine
from services.services_vending_machine import VendingMachineServices
from services.utils import Utils
from tests.routes_vending_machine.test_create_machine import TestCreateMachine

with app.app_context():
    all_machines: List[VendingMachine] = VendingMachineServices().get_all_machines()


class TestViewMachine(unittest.TestCase):
    """Test view machine with additional cases included +/- cases and testing from functions and APIs."""

    def test_view_machine_by_api_success(self) -> None:
        """Test viewing existed machine via API expected status code 200 and matching id."""
        with app.app_context():
            machine_id: int = TestCreateMachine().test_create_machine_by_api_success()
            view_machine_url = f"/machine/{machine_id}/info"
            response = app.test_client().get(view_machine_url)
            response_json = response.get_json()
            assert response.status_code == 200
            assert response_json["id"] == machine_id

    def test_view_machine_by_api_fail_no_machine(self) -> None:
        """Test viewing non-existed machine via API expected error code 404."""
        with app.app_context():
            random_id = Utils().get_invalid_machine_id()
            view_machine_url = f"/machine/{random_id}/info"
            response = app.test_client().get(view_machine_url)
        assert response.status_code == 404

    def test_view_machine_by_function_success(self) -> None:
        """Test viewing existed machine via function expected type of result be VendingMachine."""
        with app.app_context():
            machine_id: int = TestCreateMachine().test_create_machine_by_api_success()
            view_machine_response: VendingMachine = (
                VendingMachineServices().get_machine(machine_id)
            )
            assert type(view_machine_response) == VendingMachine

    def test_view_machine_by_function_fail_no_machine(self) -> None:
        """Test viewing non-existed machine via function expected error code 404."""
        with self.assertRaises(HTTPException) as http_error:
            with app.app_context():
                machine_id = Utils().get_invalid_machine_id()
                VendingMachineServices().get_machine(machine_id)
                assert http_error.exception.code == 404


if __name__ == "__main__":
    unittest.main()
