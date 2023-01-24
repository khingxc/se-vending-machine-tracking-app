import os
from test_create_machine import TestCreateMachine
import requests
import unittest
from services import utils
from dotenv import load_dotenv

load_dotenv()

local_host_address = os.environ["LOCALHOST_ADDR"]


class TestEditMachine(unittest.TestCase):
    def test_edit_machine_success(self):
        created_machine_id = TestCreateMachine().test_create_machine_success()
        new_mock_location = utils.random_string()
        edit_machine_url = f"{local_host_address}/machine/{created_machine_id}/edit"
        response = requests.post(
            url=edit_machine_url, data={"location": new_mock_location}
        )
        response_json = response.json()
        assert response.status_code == 200
        assert response_json["location"] == new_mock_location
        delete_machine_url = f"{local_host_address}/machine/{created_machine_id}/delete"
        response = requests.delete(url=delete_machine_url)
        assert response.status_code == 204

    def test_edit_machine_fail(self):
        pass


if __name__ == "__main__":
    unittest.main()
