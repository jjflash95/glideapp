import os

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

from services.constants import *
from services.expand_service import ExpandService


class EmployeeService(ExpandService):
    def __init__(self):
        super(EmployeeService, self).__init__()

        self.url = os.getenv('EMPLOYEES_API')
        self.http = self.buildclient()

    def buildclient(self, max_attempts=5):
        retry_strategy = Retry(
            total=max_attempts,
            status_forcelist=[429, 500, 502, 503, 504],
            method_whitelist=["HEAD", "GET", "OPTIONS"]
        )

        adapter = HTTPAdapter(max_retries=retry_strategy)
        http = requests.Session()
        http.mount("https://", adapter)
        http.mount("http://", adapter)
        return http

    def fetch(self, endpoint, params=None):
        url = "{}{}".format(self.url, endpoint)
        response = self.http.get(url, params=params)
        if response.status_code != 200:
            return False

        return response.json()

    def all(self, limit=100, offset=0):
        if not limit:
            limit = DEFAULT_PAGINATION
        if limit > MAX_PAGINATION_LIMIT:
            limit = MAX_PAGINATION_LIMIT
        if not offset or offset < 0:
            offset = DEFAULT_OFFSET

        params = {
            'limit': limit,
            'offset': offset,
        }

        return self.fetch('/employees', params=params)

    def get(self, employee_id):
        if not type(employee_id) == list:
            employee_id = [employee_id]

        params = {'id': eid for eid in employee_id}

        return self.fetch('/employees', params=params)
