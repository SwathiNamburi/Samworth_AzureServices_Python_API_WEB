import json
import requests

from utilities.allure_report import AllureReport
from utilities.config_reader import ConfigReader
from utilities.data_generator import DataGenerator
from utilities.file_reader import FileReader
from datetime import datetime


class APICalls:

    def get_request(self, url, headers, params=None):

        print("\n--- GET REQUEST ---")
        print(f"URL: {url}")

        if params:
            print(f"Params: {params}")

        response = requests.get(
            url=url,
            headers=headers,
            params=params
        )

        self._print_response(response)

        return response

    def post_request(
            self,
            url,
            data,
            headers,
            data_type='json'
    ):

        current_headers = headers.copy()

        payload = data

        print("\n--- POST REQUEST ---")
        print(f"URL: {url}")

        if data_type.lower() == 'json':

            current_headers['Content-Type'] = (
                'application/json'
            )

            payload = json.dumps(data)

        elif data_type.lower() == 'xml':

            current_headers['Content-Type'] = (
                'application/xml'
            )

        response = requests.post(
            url=url,
            data=payload,
            headers=current_headers
        )

        self._print_response(response)

        return response

    def _print_response(self, response):

        print("\n--- RESPONSE ---")

        print(
            f"Response Status Code: "
            f"{response.status_code}"
        )

        print(
            f"Response Time: "
            f"{response.elapsed.total_seconds()}s"
        )

        print(f"Response Body: {response.text}")

    def create_event_api_call(self,json_file):

        file_reader = FileReader()

        # ==========================================
        # CONFIG VALUES
        # ==========================================
        client_id = ConfigReader.get_api_config("CLIENT_ID")
        client_secret = ConfigReader.get_api_config("CLIENT_SECRET")

        # ==========================================
        # TEST DATA
        # ==========================================
        payload = file_reader.read_json(json_file)
        input_event_id = DataGenerator.generate_event_id()
        payload["id"] = input_event_id
        payload["time"] = DataGenerator.generate_current_timestamp()

        print(f"Generated Event ID: {payload['id']}")

        # ==========================================
        # HEADERS
        # ==========================================
        headers = {
            "Accept": "application/json",
            "client_id": client_id,
            "client_secret": client_secret
        }

        # ==========================================
        # POST REQUEST
        # ==========================================
        response = self.post_request(
            url="https://dev-x-sb-recipeprofessor-api-1dfxo1.tvhgc4.gbr-e1.cloudhub.io/api/events",
            data=payload,
            headers=headers
        )

        # ==========================================
        # VALIDATIONS
        # ==========================================
        #assert response.status_code in [200, 202]

        response_body = response.json()

        # response_event_id = response_body["id"]
        #
        # print(f"Response Event ID: {response_event_id}")
        # AllureReport.attach_text(
        #     "Create Event response ID",
        #     response_event_id
        # )

        # ==========================================
        # RETURN EVENT ID
        # ==========================================
        return response_body,input_event_id


    def get_events_api_call_without_tenantid(self,start_time):

        # ==========================================
        # CONFIG VALUES
        # ==========================================
        client_id = ConfigReader.get_api_config("CLIENT_ID")

        client_secret = ConfigReader.get_api_config("CLIENT_SECRET")

        base_url = ConfigReader.get_api_config("BASE_URL")

        # ==========================================
        # HEADERS
        # ==========================================
        headers = {
            "Accept": "application/json",
            "client_id": client_id,
            "client_secret": client_secret
        }

        print(
            f"Generated Start Time: "
            f"{start_time}"
        )
        # ==========================================
        # QUERY PARAMETERS
        # ==========================================
        params = {
            "start_time": start_time
        }

        # ==========================================
        # GET REQUEST
        # ==========================================
        response = self.get_request(
            url=f"{base_url}/api/events",
            headers=headers,
            params=params
        )

        # ==========================================
        # RESPONSE
        # ==========================================
        response_body = response.json()

        return response,response_body


    def get_events_api_call_with_tenantid(self,start_time,tenant_id):

        # ==========================================
        # CONFIG VALUES
        # ==========================================
        client_id = ConfigReader.get_api_config("CLIENT_ID")

        client_secret = ConfigReader.get_api_config("CLIENT_SECRET")

        base_url = ConfigReader.get_api_config("BASE_URL")

        # ==========================================
        # HEADERS
        # ==========================================
        headers = {
            "Accept": "application/json",
            "client_id": client_id,
            "client_secret": client_secret
        }

        print(
            f"Generated Start Time: "
            f"{start_time}"
        )
        # ==========================================
        # QUERY PARAMETERS
        # ==========================================
        params = {
            "start_time": start_time,
            "tenantid": tenant_id
        }

        # ==========================================
        # GET REQUEST
        # ==========================================
        response = self.get_request(
            url=f"{base_url}/api/events",
            headers=headers,
            params=params
        )

        # ==========================================
        # RESPONSE
        # ==========================================
        response_body = response.json()

        return response,response_body


    def get_events_api_call_with_missing_start_time(self,tenant_id):

        # ==========================================
        # CONFIG VALUES
        # ==========================================
        client_id = ConfigReader.get_api_config("CLIENT_ID")

        client_secret = ConfigReader.get_api_config("CLIENT_SECRET")

        base_url = ConfigReader.get_api_config("BASE_URL")

        # ==========================================
        # HEADERS
        # ==========================================
        headers = {
            "Accept": "application/json",
            "client_id": client_id,
            "client_secret": client_secret
        }


        # ==========================================
        # QUERY PARAMETERS
        # ==========================================
        params = {
            "tenantid": tenant_id
        }

        # ==========================================
        # GET REQUEST
        # ==========================================
        response = self.get_request(
            url=f"{base_url}/api/events",
            headers=headers,
            params=params
        )

        # ==========================================
        # RESPONSE
        # ==========================================
        response_body = response.json()

        return response,response_body


    def get_events_api_call_with_invalid_date_format(self,invalid_date_format,tenant_id):

        # ==========================================
        # CONFIG VALUES
        # ==========================================
        client_id = ConfigReader.get_api_config("CLIENT_ID")

        client_secret = ConfigReader.get_api_config("CLIENT_SECRET")

        base_url = ConfigReader.get_api_config("BASE_URL")

        # ==========================================
        # HEADERS
        # ==========================================
        headers = {
            "Accept": "application/json",
            "client_id": client_id,
            "client_secret": client_secret
        }


        # ==========================================
        # QUERY PARAMETERS
        # ==========================================
        params = {
            "start_time": invalid_date_format,
            "tenantid": tenant_id
        }

        # ==========================================
        # GET REQUEST
        # ==========================================
        response = self.get_request(
            url=f"{base_url}/api/events",
            headers=headers,
            params=params
        )

        # ==========================================
        # RESPONSE
        # ==========================================
        response_body = response.json()

        return response,response_body

    def get_payload(self, json_file):

        file_reader = FileReader()

        # Read JSON file
        payload = file_reader.read_json(json_file)

        # Generate dynamic event id
        event_id = f"evt-ing-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        input_time = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

        # Update payload
        payload["id"] = event_id
        payload["time"] = input_time

        # Convert dict -> JSON string
        payload_str = json.dumps(payload)

        return payload_str, event_id, input_time

    def get_events_api_call(
            self,
            start_time,
            tenant_id
    ):

        # ==========================================
        # CONFIG VALUES
        # ==========================================
        client_id = ConfigReader.get_api_config("CLIENT_ID")

        client_secret = ConfigReader.get_api_config("CLIENT_SECRET")

        base_url = ConfigReader.get_api_config("BASE_URL")

        # ==========================================
        # HEADERS
        # ==========================================
        headers = {
            "Accept": "application/json",
            "client_id": client_id,
            "client_secret": client_secret
        }

        # ==========================================
        # QUERY PARAMETERS
        # ==========================================
        params = {
            "start_time": start_time,
            "tenantid": tenant_id
        }

        print(f"GET Params: {params}")

        # ==========================================
        # GET REQUEST
        # ==========================================
        response = self.get_request(
            url=f"{base_url}/api/events",
            headers=headers,
            params=params
        )

        response_body = response.json()

        return response, response_body