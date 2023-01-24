import os
from test_create_machine import TestCreateMachine
import requests
import unittest
from services import utils
from dotenv import load_dotenv

load_dotenv()

local_host_address = os.environ["LOCALHOST_ADDR"]


class TestViewMachine(unittest.TestCase):
    def test_view_machine_success(self):
        created_machine_id = TestCreateMachine().test_create_machine_success()
        view_machine_url = f"{local_host_address}/machine/{created_machine_id}/info"
        response = requests.get(url=view_machine_url)
        response_json = response.json()
        assert response.status_code == 200
        assert response_json["id"] == created_machine_id
        delete_machine_url = f"{local_host_address}/machine/{created_machine_id}/delete"
        response = requests.delete(url=delete_machine_url)
        assert response.status_code == 204

    def test_view_machine_fail(self):
        pass

    def test_view_all_machine_success(self):
        pass


if __name__ == "__main__":
    unittest.main()
