import os
import unittest
from typing import List

import requests
from dotenv import load_dotenv
from werkzeug.exceptions import HTTPException

from app import app
from models.model_vending_machine import VendingMachine
from services.services_vending_machine import VendingMachineServices
from services.utils import Utils

load_dotenv()

local_host_address = os.environ["LOCALHOST_ADDR"]
view_all_machine_url = f"{local_host_address}/machine"
create_machine_url = f"{local_host_address}/machine/create"


with app.app_context():
    all_machines: List[VendingMachine] = VendingMachineServices().get_all_machines()


class TestViewMachine(unittest.TestCase):
    """Test view machine with additional cases included +/- cases and testing from functions and APIs."""

    def test_view_machine_by_api_success(self) -> None:
        """Test viewing existed machine via API expected status code 200 and matching id."""
        with app.app_context():
            machine_id = Utils().get_valid_machine_id()
            view_machine_url = f"{local_host_address}/machine/{machine_id}/info"
            response = requests.get(url=view_machine_url)
            response_json = response.json()
            assert response.status_code == 200
            assert response_json["id"] == machine_id

    def test_view_machine_by_api_fail_no_machine(self) -> None:
        """Test viewing non-existed machine via API expected error code 404."""
        with app.app_context():
            random_id = Utils().get_invalid_machine_id()
            view_machine_url = f"{local_host_address}/machine/{random_id}/info"
            response = requests.get(url=view_machine_url)
        assert response.status_code == 404

    def test_view_all_machine_by_api_success(self) -> None:
        """Test viewing all created machine via API expected response to be similar to the one from calling function."""
        with app.app_context():
            machines_response_json = (requests.get(url=view_all_machine_url)).json()
            machines_from_db = Utils().filter_list(data="machines")
            machines_serializers = [
                machine.serializer() for machine in machines_from_db
            ]
            for machine in machines_response_json:
                assert machine in machines_serializers

    def test_view_machine_by_function_success(self) -> None:
        """Test viewing existed machine via function expected type of result be VendingMachine."""
        with app.app_context():
            machine_id = Utils().get_valid_machine_id()
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

    def test_view_all_machine_by_function_success(self) -> None:
        """Test viewing all created machines via function expected machines from function to be similar to response."""
        with app.app_context():
            machines_response_json = (requests.get(url=view_all_machine_url)).json()
            machines_from_function = VendingMachineServices().get_all_machines()
            machines_serializers = [
                machine.serializer() for machine in machines_from_function
            ]
            for machine in machines_response_json:
                assert machine in machines_serializers


if __name__ == "__main__":
    unittest.main()
