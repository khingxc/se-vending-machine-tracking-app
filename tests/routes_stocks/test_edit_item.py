import os
import random
import unittest
import requests
from services import utils
from dotenv import load_dotenv
from tests.routes_vending_machine.test_create_machine import TestCreateMachine

load_dotenv()

local_host_address = os.environ["LOCALHOST_ADDR"]


class TestEditItem(unittest.TestCase):
    def test_edit_item_success(self):
        created_machine_id = TestCreateMachine().test_create_machine_success()
        mock_item = utils.random_string()
        mock_amount = random.randint(1, 10)
        add_item_url = f"{local_host_address}/machine/{created_machine_id}/add_item"
        response_create = requests.post(
            url=add_item_url, data={"product": mock_item, "amount": mock_amount}
        )
        assert response_create.status_code == 201
        edit_item_url = f"{local_host_address}/machine/{created_machine_id}/edit_item"
        mock_amount = random.randint(25, 50)
        response_edit_item = requests.post(
            url=edit_item_url, data={"product": mock_item, "amount": mock_amount}
        )
        assert response_edit_item.status_code == 200
        delete_item_url = (
            f"{local_host_address}/machine/{created_machine_id}/delete_item"
        )
        response_delete = requests.delete(
            url=delete_item_url, data={"product": mock_item}
        )
        assert response_delete.status_code == 204

    def test_edit_item_fail_no_params(self):
        view_all_machine_url = f"{local_host_address}/machine"
        machines_response = (requests.get(url=view_all_machine_url)).json()
        if len(machines_response) == 0:
            machine_id = TestCreateMachine().test_create_machine_success()
        else:
            machine_id = random.choice(machines_response)["id"]
        edit_item_url = f"{local_host_address}/machine/{machine_id}/edit_item"
        response_edit_item = requests.post(url=edit_item_url, data={"product": "", "amount": 0})
        assert response_edit_item.status_code == 400

    def test_edit_item_fail_no_machine(self):
        view_all_machine_url = f"{local_host_address}/machine"
        machines_response = (requests.get(url=view_all_machine_url)).json()
        machine_ids = [machine["id"] for machine in machines_response]
        random_id = random.randint(0, max(machine_ids) * 10)
        mock_item = utils.random_string()
        mock_amount = random.randint(25, 50)
        while random_id in machine_ids:
            random_id = random.randint(0, max(machine_ids) * 10)
        edit_item_url = f"{local_host_address}/machine/{random_id}/edit_item"
        response_edit_item = requests.post(url=edit_item_url, data={"product": mock_item, "amount": mock_amount})
        assert response_edit_item.status_code == 404



if __name__ == "__main__":
    unittest.main()
