import os
import requests
import unittest
from services import utils
from dotenv import load_dotenv

load_dotenv()

local_host_address = os.environ["LOCALHOST_ADDR"]

create_machine_url = f"{local_host_address}/machine/create"


class TestCreateMachine(unittest.TestCase):
    def test_create_machine_success(self):
        mock_location = utils.random_string()
        response = requests.post(
            url=create_machine_url, data={"location": mock_location}
        )
        response_json = response.json()
        assert response.status_code == 201
        assert response_json["location"] == mock_location
        return response_json["id"]

    def test_create_machine_fail(self):
        response = requests.post(url=create_machine_url)
        assert response.status_code == 400


if __name__ == "__main__":
    unittest.main()
