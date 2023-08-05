"""Orquestador API client"""
import os

import requests
from decouple import config
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


class OrquestadorAPI:
    """Orquestador API client"""

    # BASE_URL = f"{config('TARGET_DOMAIN')}/api"
    BASE_URL = f"https://{config('TARGET_DOMAIN')}/api"
    TARGET_USERNAME = config("TARGET_USERNAME")
    TARGET_PASSWORD = config("TARGET_PASSWORD")

    def __init__(self, transition_id=None, token=None):
        self.t_id = transition_id
        if token:
            self._token = token
        else:
            self.authenticate()

    def get_url(self, url):
        return f"{self.BASE_URL}/{url}"

    def authenticate(self):
        """Login to orquestador"""
        url = self.get_url("auth/token/")

        payload = {"username": self.TARGET_USERNAME, "password": self.TARGET_PASSWORD}
        headers = {"accept": "application/json", "Content-Type": "application/json"}

        response = requests.request("POST", url, headers=headers, json=payload)

        if response.status_code in [200, 201]:
            self._token = response.json()["accessToken"]
        else:
            raise Exception(response.json())

    def make_request(self, request_type, url, payload=None, headers=None, files=None):
        """Generic HTTP adapter for orquestador"""

        url = self.get_url(url)

        if headers is None:
            headers = {}
        retry_strategy = Retry(total=3, status_forcelist=[429, 500, 502, 503, 504])
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session = requests.Session()
        session.mount("https://", adapter)

        response = session.request(request_type, url, headers=headers, data=payload, files=files)
        return response

    def make_authenticated_request(self, request_type, url, payload=None, files=None):
        """Generic HTTP Adapter for authenticated requests to orquestador"""

        headers = {
            "Authorization": f"Token {self._token}",
        }

        response = self.make_request(request_type, url, payload=payload, headers=headers, files=files)
        return response

    def _transition(self, data):
        """Patch data into a transition"""
        url = f"transition/{self.t_id}"

        response = self.make_request("PATCH", url, data)
        return response

    def _transition_v1(self, data, files=None):
        """POST data into a transition v1"""
        url = f"v1/transition/{self.t_id}/"

        response = self.make_authenticated_request("POST", url, payload=data, files=files)

        return response

    def log_records(self, records):
        """Log records into transition"""
        data = {"console": records}
        response = self._transition_v1(data)
        return response

    def send_log_files(self, log_path, report_path):
        files = [
            (
                'log_file',
                (
                    'log.html',
                    open(log_path, 'rb'),
                    'text/html'
                )
            ),
            (
                'report_file',
                (
                    'report.html',
                    open(report_path, 'rb'),
                    'text/html')
            )
        ]

        result = self._transition_v1({}, files=files)
        print(result)
        print(result.text)

    def send_status(self, status, message):
        data = {"status": status, "message": message}
        self._transition_v1(data)

    def send_status_logs(self, log_path, report_path, status, message):
        files = [
            (
                'log_file',
                (
                    'log.html',
                    open(log_path, 'rb'),
                    'text/html'
                )
            ),
            (
                'report_file',
                (
                    'report.html',
                    open(report_path, 'rb'),
                    'text/html')
            )
        ]
        data = {"status": status, "message": message}
        print(data)
        result = self._transition_v1(data, files=files)
        print(result)
        print(result.text)

    def send_logs_infra(self, logs):
        data = {"infra_logs": logs}
        self._transition_v1(data)

    def send_status_logs_infra(self, logs, status, message):
        data = {"infra_logs": logs, "status": status, "message": message}
        self._transition_v1(data)

    def output_process_instance(self, data):
        url = f"v1/instance/output/"
        response = self.make_authenticated_request("POST", url, data)
        return response

    def ping(self):
        """Ensure connection to orquestador is still alive"""
        data = {"alive": True}
        response = self._transition_v1(data)

    def get_secret(self, secret_name):
        url = f"v1/secret/"
        data = {
            "workspace_token": os.getenv("RPAMAKER_TOKEN"),
            "company_token": os.getenv("COMPANY_TOKEN"),
            "secret_key": secret_name
        }
        response = self.make_authenticated_request("POST", url, data)
        return response.json()


def send_result(result, id_pi):
    print('Sending result to RPAMAKER')
    data = {"instance_id": id_pi, "meta": {"result": result}}
    OrquestadorAPI().output_process_instance(data)


def get_secret(secret_name):
    return OrquestadorAPI().get_secret(secret_name)
