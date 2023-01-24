import os
import random
import unittest
import requests
from services import utils
from dotenv import load_dotenv
from tests.routes_vending_machine.test_create_machine import TestCreateMachine

load_dotenv()

local_host_address = os.environ["LOCALHOST_ADDR"]


class TestDeleteItem(unittest.TestCase):
    def test_delete_item_success(self):
        created_machine_id = TestCreateMachine().test_create_machine_success()
        mock_item = utils.random_string()
        mock_amount = random.randint(1, 10)
        add_item_url = f"{local_host_address}/machine/{created_machine_id}/add_item"
        response_create = requests.post(
            url=add_item_url, data={"product": mock_item, "amount": mock_amount}
        )
        assert response_create.status_code == 201
        delete_item_url = (
            f"{local_host_address}/machine/{created_machine_id}/delete_item"
        )
        response_delete = requests.delete(
            url=delete_item_url, data={"product": mock_item}
        )
        assert response_delete.status_code == 204

    def test_delete_item_fail_no_params(self):
        created_machine_id = TestCreateMachine().test_create_machine_success()
        mock_item = utils.random_string()
        mock_amount = random.randint(1, 10)
        add_item_url = f"{local_host_address}/machine/{created_machine_id}/add_item"
        response_create = requests.post(
            url=add_item_url, data={"product": mock_item, "amount": mock_amount}
        )
        assert response_create.status_code == 201
        delete_item_url = (
            f"{local_host_address}/machine/{created_machine_id}/delete_item"
        )
        response_delete = requests.delete(url=delete_item_url)
        assert response_delete.status_code == 400


if __name__ == "__main__":
    unittest.main()
