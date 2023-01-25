import os
import random
import requests
import unittest
from dotenv import load_dotenv
from services import utils

load_dotenv()

local_host_address = os.environ["LOCALHOST_ADDR"]

class TestDeleteMachine(unittest.TestCase):
    def test_delete_machine_success(self):
        view_all_machine_url = f"{local_host_address}/machine"
        machines_response = (requests.get(url=view_all_machine_url)).json()
        if len(machines_response) == 0:
            create_machine_url = f"{local_host_address}/machine/create"
            mock_location = utils.random_string()
            response_json = (requests.post(
                url=create_machine_url, data={"location": mock_location}
            )).json()
            machine_id = response_json["id"]
        else:
            machine_id = random.choice(machines_response)["id"]
        delete_machine_url = f"{local_host_address}/machine/{machine_id}/delete"
        response = requests.delete(url=delete_machine_url)
        assert response.status_code == 204

    def test_delete_machine_fail_no_machine(self):
        view_all_machine_url = f"{local_host_address}/machine"
        machines_response = (requests.get(url=view_all_machine_url)).json()
        machine_ids = [machine["id"] for machine in machines_response]
        random_id = random.randint(0, max(machine_ids)*10)
        while random_id in machine_ids:
            random_id = random.randint(0, max(machine_ids)*10)
        delete_machine_url = f"{local_host_address}/machine/{random_id}/delete"
        response = requests.delete(url=delete_machine_url)
        assert response.status_code == 404


if __name__ == "__main__":
    unittest.main()
