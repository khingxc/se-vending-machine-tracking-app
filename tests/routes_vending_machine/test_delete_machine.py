import os
import requests
import unittest
from dotenv import load_dotenv
from test_create_machine import TestCreateMachine

load_dotenv()

local_host_address = os.environ["LOCALHOST_ADDR"]


class TestDeleteMachine(unittest.TestCase):
    def test_delete_machine_success(self):
        created_machine_id = TestCreateMachine().test_create_machine_success()
        delete_machine_url = f"{local_host_address}/machine/{created_machine_id}/delete"
        response = requests.delete(url=delete_machine_url)
        assert response.status_code == 204

    def test_delete_machine_fail_no_machine(self):
        pass


if __name__ == "__main__":
    unittest.main()
