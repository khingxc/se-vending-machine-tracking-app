import os
import random
import unittest
import requests
from services import utils
from dotenv import load_dotenv
from tests.routes_vending_machine.test_create_machine import TestCreateMachine

load_dotenv()

local_host_address = os.environ["LOCALHOST_ADDR"]


class TestAddItem(unittest.TestCase):
    def test_add_item_success(self):
        created_machine_id = TestCreateMachine().test_create_machine_success()
        mock_item = utils.random_string()
        mock_amount = random.randint(1, 10)
        add_item_url = f"{local_host_address}/machine/{created_machine_id}/add_item"
        response = requests.post(
            url=add_item_url, data={"product": mock_item, "amount": mock_amount}
        )
        response_json = response.json()
        assert response.status_code == 201
        assert response_json["product"] == mock_item
        assert response_json["amount"] == mock_amount
        delete_machine_url = f"{local_host_address}/machine/{created_machine_id}/delete"
        response = requests.delete(url=delete_machine_url)
        assert response.status_code == 204

    def test_add_item_fail_no_params(self):
        created_machine_id = TestCreateMachine().test_create_machine_success()
        add_item_url = f"{local_host_address}/machine/{created_machine_id}/add_item"
        response = requests.post(url=add_item_url)
        assert response.status_code == 400

    def test_add_item_fail_no_machine(self):
        pass


if __name__ == "__main__":
    unittest.main()
