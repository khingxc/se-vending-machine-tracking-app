import os
import unittest
from typing import List

import requests
from dotenv import load_dotenv
from requests import Response
from werkzeug.exceptions import HTTPException

from app import app
from models.model_vending_machine import VendingMachine
from services.services_vending_machine import VendingMachineServices
from services.utils import Utils, random_string

load_dotenv()

local_host_address = os.environ["LOCALHOST_ADDR"]

with app.app_context():
    all_machines: List[VendingMachine] = Utils().filter_list("machines")


class TestEditMachine(unittest.TestCase):
    """Test edit machine with additional cases included +/- cases and testing from functions and APIs."""

    def test_edit_machine_by_api_success(self) -> None:
        """Test editing machine with all requirements via API expected status code 200."""
        with app.app_context():
            machine_id: int = Utils().get_valid_machine_id()
            new_mock_location: str = random_string()
            edit_machine_url: str = f"{local_host_address}/machine/{machine_id}/edit"
            response: Response = requests.post(
                url=edit_machine_url, data={"location": new_mock_location}
            )
            response_json = response.json()
            assert response.status_code == 200
            assert response_json["location"] == new_mock_location

    def test_edit_machine_by_api_fail_no_params(self) -> None:
        """Test editing machine with no param via API expected error code 400 (bad request)."""
        with app.app_context():
            machine_id: int = Utils().get_valid_machine_id()
            edit_machine_url: str = f"{local_host_address}/machine/{machine_id}/edit"
            response: Response = requests.post(url=edit_machine_url)
            assert response.status_code == 400

    def test_edit_machine_by_api_fail_no_machine(self) -> None:
        """Test editing non-existed machine with all requirements via API expected error code 404."""
        with app.app_context():
            invalid_machine_id: int = Utils().get_invalid_machine_id()
            new_mock_location: str = random_string()
            edit_machine_url: str = (
                f"{local_host_address}/machine/{invalid_machine_id}/edit"
            )
            response: Response = requests.post(
                url=edit_machine_url, data={"location": new_mock_location}
            )
            assert response.status_code == 404

    def test_edit_machine_by_function_success(self) -> None:
        """Test editing machine with all requirements via function expected status code 200."""
        with app.app_context():
            machine_id: int = Utils().get_valid_machine_id()
            new_mock_location: str = random_string()
            edit_machine_result = VendingMachineServices().edit_machine(
                machine_id, new_mock_location
            )
            saved_location: str = edit_machine_result.location
            assert type(edit_machine_result) == VendingMachine
            assert saved_location == new_mock_location

    def test_edit_machine_by_function_fail_no_location(self) -> None:
        """Test editing existed machine with no data via function expected error code 400."""
        with self.assertRaises(HTTPException) as http_error:
            with app.app_context():
                machine_id: int = Utils().get_valid_machine_id()
                VendingMachineServices().edit_machine(machine_id, "")
            assert http_error.exception.code == 400

    def test_edit_machine_by_function_fail_no_machine(self) -> None:
        """Test editing non-existed machine with all requirements via function expected status code 404."""
        with self.assertRaises(HTTPException) as http_error:
            with app.app_context():
                mock_location: str = random_string()
                machine_id: int = Utils().get_invalid_machine_id()
                VendingMachineServices().edit_machine(machine_id, mock_location)
            assert http_error.exception.code == 404


if __name__ == "__main__":
    unittest.main()
