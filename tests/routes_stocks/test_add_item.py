import os
import random
import unittest
import requests
from services import utils
from dotenv import load_dotenv
from tests.routes_vending_machine.test_create_machine import TestCreateMachine

load_dotenv()

local_host_address = os.environ["LOCALHOST_ADDR"]
view_all_machine_url = f"{local_host_address}/machine"
machines_response = (requests.get(url=view_all_machine_url)).json()


class TestAddItem(unittest.TestCase):
    def test_add_item_success(self):
        if len(machines_response) == 0:
            machine_id = TestCreateMachine().test_create_machine_success()
        else:
            machine_id = random.choice(machines_response)["id"]
        mock_item = utils.random_string()
        mock_amount = random.randint(1, 10)
        add_item_url = f"{local_host_address}/machine/{machine_id}/add-item"
        response = requests.post(
            url=add_item_url, data={"product": mock_item, "amount": mock_amount}
        )
        response_json = response.json()
        assert response.status_code == 201
        assert response_json["product"] == mock_item
        assert response_json["amount"] == mock_amount

    def test_add_item_fail_no_params(self):
        if len(machines_response) == 0:
            machine_id = TestCreateMachine().test_create_machine_success()
        else:
            machine_id = random.choice(machines_response)["id"]
        add_item_url = f"{local_host_address}/machine/{machine_id}/add-item"
        response = requests.post(url=add_item_url, data={"product": "", "amount": 0})
        assert response.status_code == 400

    def test_add_item_fail_no_machine(self):
        machine_ids = [machine["id"] for machine in machines_response]
        random_id = random.randint(0, max(machine_ids) * 10)
        while random_id in machine_ids:
            random_id = random.randint(0, max(machine_ids) * 10)
        mock_item = utils.random_string()
        mock_amount = random.randint(1, 10)
        add_item_url = f"{local_host_address}/machine/{random_id}/add-item"
        response = requests.post(
            url=add_item_url, data={"product": mock_item, "amount": mock_amount}
        )
        assert response.status_code == 404


if __name__ == "__main__":
    unittest.main()
