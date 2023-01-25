import os
import random
import requests
import unittest
from services.utils import random_string
from dotenv import load_dotenv

load_dotenv()

local_host_address = os.environ["LOCALHOST_ADDR"]


class TestEditMachine(unittest.TestCase):
    def test_edit_machine_success(self):
        view_all_machine_url = f"{local_host_address}/machine"
        machines_response = (requests.get(url=view_all_machine_url)).json()
        if len(machines_response) == 0:
            machine_id = random.choice(machines_response)["id"]
        else:
            create_machine_url = f"{local_host_address}/machine/create"
            mock_location = random_string()
            response_json = (requests.post(
                url=create_machine_url, data={"location": mock_location}
            )).json()
            machine_id = response_json["id"]
        new_mock_location = random_string()
        edit_machine_url = f"{local_host_address}/machine/{machine_id}/edit"
        response = requests.post(
            url=edit_machine_url, data={"location": new_mock_location}
        )
        response_json = response.json()
        assert response.status_code == 200
        assert response_json["location"] == new_mock_location

    def test_edit_machine_fail_no_params(self):
        view_all_machine_url = f"{local_host_address}/machine"
        machines_response = (requests.get(url=view_all_machine_url)).json()
        if len(machines_response) == 0:
            machine_id = random.choice(machines_response)["id"]
        else:
            create_machine_url = f"{local_host_address}/machine/create"
            mock_location = random_string()
            response_json = (requests.post(
                url=create_machine_url, data={"location": mock_location}
            )).json()
            machine_id = response_json["id"]
        edit_machine_url = f"{local_host_address}/machine/{machine_id}/edit"
        response = requests.post(url=edit_machine_url)
        assert response.status_code == 400

    def test_edit_machine_fail_no_machine(self):
        view_all_machine_url = f"{local_host_address}/machine"
        machines_response = (requests.get(url=view_all_machine_url)).json()
        machine_ids = [machine["id"] for machine in machines_response]
        random_id = random.randint(0, max(machine_ids) * 10)
        while random_id in machine_ids:
            random_id = random.randint(0, max(machine_ids) * 10)
        new_mock_location = random_string()
        edit_machine_url = f"{local_host_address}/machine/{random_id}/edit"
        response = requests.post(
            url=edit_machine_url, data={"location": new_mock_location}
        )
        assert response.status_code == 404


if __name__ == "__main__":
    unittest.main()
