import os
import unittest

import requests
from dotenv import load_dotenv
from werkzeug.exceptions import HTTPException

from app import app
from models.model_vending_machine import VendingMachine
from services import utils
from services.services_vending_machine import VendingMachineServices

load_dotenv()

local_host_address = os.environ["LOCALHOST_ADDR"]

create_machine_url = f"{local_host_address}/machine/create"


class TestCreateMachine(unittest.TestCase):
    """Test create machine with additional cases included +/- cases and testing from functions and APIs."""

    def test_create_machine_by_api_success(self) -> None:
        """Test creating machine via API with valid param expected create successfully with matching results."""
        mock_location = utils.random_string()
        response = requests.post(
            url=create_machine_url, data={"location": mock_location}
        )
        response_json = response.json()
        assert response.status_code == 201
        assert response_json["location"] == mock_location
        return response_json["id"]

    def test_create_machine_by_api_fail(self) -> None:
        """Test creating machine via API with no param expected error code 400."""
        response = requests.post(url=create_machine_url)
        assert response.status_code == 400

    def test_create_machine_by_function_success(self) -> None:
        """Test creating machine with valid param via function, expected a match result."""
        mock_location: str = utils.random_string()
        with app.app_context():
            new_machine: VendingMachine = VendingMachineServices().create_machine(
                mock_location
            )
            new_machine_serializer: dict[str, int] = new_machine.serializer()
            assert new_machine_serializer["location"] == mock_location

    def test_create_machine_by_function_fail(self) -> None:
        """Test creating machine with no param via function expected error code 400."""
        with self.assertRaises(HTTPException) as http_error:
            with app.app_context():
                VendingMachineServices().create_machine("")
            assert http_error.exception.code == 400


if __name__ == "__main__":
    unittest.main()
