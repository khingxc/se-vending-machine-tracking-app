import os
from app import app
import random
import requests
import unittest
from dotenv import load_dotenv
from services.utils import random_string, Utils

load_dotenv()

local_host_address = os.environ["LOCALHOST_ADDR"]


class TestViewMachine(unittest.TestCase):
    def test_view_machine_success(self):
        view_all_machine_url = f"{local_host_address}/machine"
        machines_response = (requests.get(url=view_all_machine_url)).json()
        if len(machines_response) == 0:
            create_machine_url = f"{local_host_address}/machine/create"
            mock_location = random_string()
            response_json = (
                requests.post(url=create_machine_url, data={"location": mock_location})
            ).json()
            machine_id = response_json["id"]
        else:
            machine_id = random.choice(machines_response)["id"]
        view_machine_url = f"{local_host_address}/machine/{machine_id}/info"
        response = requests.get(url=view_machine_url)
        response_json = response.json()
        assert response.status_code == 200
        assert response_json["id"] == machine_id

    def test_view_machine_fail_no_machine(self):
        view_all_machine_url = f"{local_host_address}/machine"
        machines_response = (requests.get(url=view_all_machine_url)).json()
        machine_ids = [machine["id"] for machine in machines_response]
        random_id = random.randint(0, max(machine_ids) * 10)
        while random_id in machine_ids:
            random_id = random.randint(0, max(machine_ids) * 10)
        view_machine_url = f"{local_host_address}/machine/{random_id}/info"
        response = requests.get(url=view_machine_url)
        assert response.status_code == 404

    def test_view_all_machine_success(self):
        view_all_machine_url = f"{local_host_address}/machine"
        machines_response_json = (requests.get(url=view_all_machine_url)).json()
        with app.app_context():
            machines_from_db = Utils().filter_list(data="machine")
        machines_serializers = [machine.serializer() for machine in machines_from_db]
        assert machines_serializers == machines_response_json


if __name__ == "__main__":
    unittest.main()
