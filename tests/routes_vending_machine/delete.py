import os
import requests
import unittest
from dotenv import load_dotenv
import create

load_dotenv()

local_host_address = os.environ["LOCALHOST_ADDR"]


class TestDeleteMachine(unittest.TestCase):

    def test_delete_machine_success(self):
        created_machine_id = create.TestCreateMachine().test_create_machine_success()
        delete_machine_url = f"{local_host_address}/machine/{created_machine_id}/delete"
        response = requests.delete(url=delete_machine_url)
        assert response.status_code == 204


if __name__ == '__main__':
    unittest.main()







