from abc import abstractmethod, ABC
from time import sleep

import urllib3
import requests

from netorca_sdk.config import RETRY_TIMES, AUTH_ENDPOINT, TEAM_ENDPOINT
from netorca_sdk.exceptions import NetorcaException

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class AbstractNetorcaAuth(ABC):
    @abstractmethod
    def get(self, *args, **kwargs):
        ...

    @abstractmethod
    def post(self, *args, **kwargs):
        ...

    @abstractmethod
    def put(self, *args, **kwargs):
        ...

    @abstractmethod
    def patch(self, *args, **kwargs):
        ...

    @abstractmethod
    def delete(self, *args, **kwargs):
        ...


class NetorcaAuth(AbstractNetorcaAuth):
    def __init__(self, fqdn, username=None, password=None, api_key=None):
        self.username = username
        self.password = password
        self.api_key = api_key
        self.fqdn = fqdn
        self.headers = {
            'content-type': 'application/json'
        }

        if self.username and self.password:
            self.token = self.get_auth_token()
            self.headers['Authorization'] = f'Token {self.token}'
        elif self.api_key:
            self.headers['Authorization'] = f'Api-Key {self.api_key}'
        else:
            raise NetorcaException(
                f"Failed to authenticate. You must provide either (username and password) or API KEY")

    def get(self, *args, **kwargs):
        url = kwargs.get("url")
        filters = kwargs.get("filters")
        authentication_required = kwargs.get("authentication_required", False)

        if not url:
            raise NetorcaException(f"URL not provided!")

        for retry in range(RETRY_TIMES):
            if authentication_required:
                response = requests.get(url=url, headers=self.headers, verify=False, params=filters)
            else:
                response = requests.get(url=url, verify=False, params=filters)
            if 200 <= response.status_code < 500:
                return response
            sleep(retry)
        raise NetorcaException(
            f"Failed to send GET request. GET details: {args, kwargs}. Response details: {response.json()}")

    def post(self, *args, **kwargs):
        url = kwargs.get("url")
        data = kwargs.get("data")
        authentication_required = kwargs.get("authentication_required", False)

        if not url or not data:
            raise NetorcaException(f"URL or data not provided!")

        if authentication_required:
            response = requests.post(url=url, data=data, headers=self.headers, verify=False)
        else:
            response = requests.post(url=url, data=data, verify=False)

        if 200 <= response.status_code < 500:
            return response
        raise NetorcaException(
            f"Failed to send POST request. POST details: {args, kwargs}. Response details: {response.json()}")

    def put(self, *args, **kwargs):
        url = kwargs.get("url")
        data = kwargs.get("data")
        authentication_required = kwargs.get("authentication_required", False)

        if not url or not data:
            raise NetorcaException(f"URL or data not provided!")

        if authentication_required:
            response = requests.put(url=url, data=data, headers=self.headers, verify=False)
        else:
            response = requests.put(url=url, data=data, verify=False)
        if 200 <= response.status_code < 500:
            return response
        raise NetorcaException(
            f"Failed to send PUT request. PUT details: {args, kwargs}. Response details: {response.json()}")

    def patch(self, *args, **kwargs):
        url = kwargs.get("url")
        data = kwargs.get("data")
        authentication_required = kwargs.get("authentication_required", False)

        if not url or not data:
            raise NetorcaException(f"URL or data not provided!")

        if authentication_required:
            response = requests.patch(url=url, data=data, headers=self.headers, verify=False)
        else:
            response = requests.patch(url=url, data=data, verify=False)
        if 200 <= response.status_code < 500:
            return response
        raise NetorcaException(
            f"Failed to send PATCH request. PATCH details: {args, kwargs}. Response details: {response.json()}")

    def delete(self, *args, **kwargs):
        NetorcaException("Not implemented.")

    def get_auth_token(self) -> str:
        AUTH_URL = f"{self.fqdn}{AUTH_ENDPOINT}"

        data = {
            "username": self.username,
            "password": self.password
        }
        response = self.post(url=AUTH_URL, data=data, verify=False)
        if response.status_code == 200:
            return response.json()['token']
        raise NetorcaException(f"Authentication failed due to: {response.json()}")

    def refresh_auth_token(self):
        return self.get_auth_token()

    def get_teams_info(self) -> list:
        """ Get team info for given user"""
        TEAM_URL = f"{self.fqdn}{TEAM_ENDPOINT}"
        response = self.get(url=TEAM_URL, authentication_required=True)
        if response.status_code == 200:
            return response.json()['results']
        raise NetorcaException(f"Error fetching team info.")

    def __str__(self):
        return f"Username: {self.username}, netorca instance: {self.fqdn}."

    def __repr__(self):
        return f"Username: {self.username}, netorca instance: {self.fqdn}."
