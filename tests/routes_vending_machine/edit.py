import os
import create
import requests
import unittest
from services import utils
from dotenv import load_dotenv

load_dotenv()

local_host_address = os.environ["LOCALHOST_ADDR"]


class TestEditMachine(unittest.TestCase):

    def test_edit_machine_success(self):
        created_machine_id = create.TestCreateMachine().test_create_machine_success()
        new_mock_location = utils.random_string()
        edit_machine_url = f"{local_host_address}/machine/{created_machine_id}/edit"
        response = requests.post(url=edit_machine_url, data={"location": new_mock_location})
        response_json = response.json()
        assert response.status_code == 200
        assert response_json["location"] == new_mock_location


if __name__ == '__main__':
    unittest.main()
