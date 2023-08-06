import json
import os
from typing import Tuple

import yaml
from beautifultable import BeautifulTable

from netorca_sdk.auth import AbstractNetorcaAuth, NetorcaAuth
from netorca_sdk.config import VALIDATE_CONSUMER_SUBMISSION_ENDPOINT, SUBMIT_CONSUMER_SUBMISSION_ENDPOINT
from netorca_sdk.exceptions import NetorcaException


class ConsumerSubmission:
    def __init__(self, netorca_api_key: str):
        self.netorca_api_key = netorca_api_key

        self.config = None
        self.consumer_submission = None
        self.auth = None

    def load_from_repository(self, repository_path: str) -> None:
        """
            Check if valid and load request and config from consumer's repository.
            Repository must contain `.netorca` directory and `config.yaml` file.
            Note: Only one allowed extensions in `.netorca` directory is `*.yaml`

            Args:
                repository_path: str    path to consumer repository

            Returns: None
        """
        repository_exists = os.path.isdir(repository_path)
        if not repository_exists:
            raise NetorcaException(
                f"`{repository_path}` directory does not exist.")
        netorca_exists = os.path.isdir(f"{repository_path}/.netorca")
        if not netorca_exists:
            raise NetorcaException("`.netorca` directory does not exist.")

        dotnetorca_path = f"{repository_path}/.netorca"

        # check and load config
        with open(f"{repository_path}/.netorca/config.yaml", "r") as stream:
            try:
                config = yaml.safe_load(stream)
                netorca_global = config.get("netorca_global", {})
                if not (netorca_global or netorca_global.get("base_url")):
                    raise NetorcaException(
                        "No `netorca_global.base_url` provided.")

                self.config = config
                self.auth = self.get_auth()
            except yaml.YAMLError as exc:
                raise NetorcaException(
                    f"Error while parsing file: `config.yml`. Exception: {exc.problem}")

        _tmp_consumer_submission = {}
        # check and load consumer request
        for filename in os.listdir(dotnetorca_path):
            if filename == "config.yaml":
                continue

            f = os.path.join(dotnetorca_path, filename)
            # checking if it is a file and is `*.yaml`
            if not (os.path.isfile(f) and f.endswith('.yaml')):
                raise NetorcaException(
                    f"Consumer request files must have `.yaml` extension")

            with open(f, "r") as stream:
                try:
                    app = yaml.safe_load(stream)
                except yaml.YAMLError as exc:
                    raise NetorcaException(
                        f"Error while parsing file: `{filename}`. Exception: {exc.problem}")

                for key in app.keys():
                    if key in _tmp_consumer_submission:
                        raise NetorcaException(
                            f"Application with name `{key}` already exists in different `.yaml` declaration.")

                _tmp_consumer_submission.update(app)
        self.consumer_submission = _tmp_consumer_submission

    def get_auth(self) -> AbstractNetorcaAuth:
        if not self.config:
            raise NetorcaException(f"Cannot authenticate before loading repository config.")

        netorca_fqdn = self.config.get("netorca_global", {}).get("base_url")
        self.auth = NetorcaAuth(fqdn=netorca_fqdn, api_key=self.netorca_api_key)
        return self.auth

    def get_team(self) -> dict:
        teams = self.auth.get_teams_info()
        if teams:
            return teams[0]
        return {}

    def prepare_request(self) -> dict:
        team = self.get_team()
        metadata = self.config.get("netorca_global", {}).get("metadata", {})

        if not (team and self.config and self.consumer_submission and self.auth):
            raise NetorcaException(
                "Team, config and consumer request should be fetched at this stage.")

        full_request = {
            team['name']: {
                "metadata": metadata,
                **self.consumer_submission
            }
        }
        return full_request

    def validate(self, pretty_print=False) -> Tuple[bool, dict]:
        """
            Validate consume request.
            NOTE: Data must be first imported with `load_from_repository` method

            Returns:
                Tuple[bool, str]    ->  is_valid, validation_errors
        """
        if not (self.config and self.consumer_submission and self.auth):
            raise NetorcaException(f"Use `load_from_repository(repository_path)` method to load configuration.")
        VALIDATE_REQUEST_PATH = f"{self.auth.fqdn}{VALIDATE_CONSUMER_SUBMISSION_ENDPOINT}"
        full_request = self.prepare_request()

        response = self.auth.post(url=VALIDATE_REQUEST_PATH, data=json.dumps(full_request),
                                  authentication_required=True)

        response = response.json()
        if response.get("is_valid"):
            return True, {}
        errors = response.get("errors")

        if pretty_print:
            ConsumerSubmission.pretty_print_errors(errors)
        return False, errors

    def submit(self) -> Tuple[bool, str]:
        """
            Validate and submit consumer request.
            NOTE: Data must be first imported with `load_from_repository` method

            Returns:
                bool, str    ->  submission successful, submission messages
        """
        is_valid = self.validate(pretty_print=True)
        if not is_valid[0]:
            return False, "Consumer request is invalid and cannot be submitted."

        SUBMIT_REQUEST_PATH = f"{self.auth.fqdn}{SUBMIT_CONSUMER_SUBMISSION_ENDPOINT}"
        full_request = self.prepare_request()
        response = self.auth.post(url=SUBMIT_REQUEST_PATH, data=json.dumps(full_request),
                                  authentication_required=True)
        if response.status_code == 201:
            return True, "Submitted successfuly."
        return False, response.text

    @staticmethod
    def pretty_print_errors(errors: dict) -> None:
        """
            Pretty print errors
            #TODO: this should be refactored to cleaner code (probably recursive)
        """

        table = BeautifulTable(maxwidth=100)
        table.set_style(BeautifulTable.STYLE_SEPARATED)
        table.columns.header = ["Team", "Field", "Reason"]
        for item1, value1 in errors.items():
            if isinstance(value1, str) or isinstance(value1, list):
                table.rows.append([item1, "", value1])
            elif isinstance(value1, dict):
                for item2, value2 in value1.items():
                    if isinstance(value2, str) or isinstance(value2, list):
                        table.rows.append([item1, item2, value2])

                        if table.rows:
                            print("-" * 100)
                            print(f"Team: {item1} validation errors")
                            print("-" * 100)
                            print(table)
                            print()
                        break

        for item1, value1 in errors.items():
            if isinstance(value1, dict):
                for item2, value2 in value1.items():
                    table = BeautifulTable(maxwidth=100)
                    table.set_style(BeautifulTable.STYLE_SEPARATED)
                    table.columns.header = ["Application", "Service", "ServiceItem", "Field", "Reason"]

                    if isinstance(value2, dict):
                        for item3, value3 in value2.items():
                            if isinstance(value3, str):
                                table.rows.append([item2, "", "", item3, value3])
                            elif isinstance(value3, list):
                                for err in value3:
                                    table.rows.append([item2, "", "", item3, err])
                            elif isinstance(value3, dict):
                                for item4, value4 in value3.items():
                                    if isinstance(value4, str) or isinstance(value4, list):
                                        table.rows.append([item2, item3, "", item4, value4])
                                    elif isinstance(value4, dict):
                                        for item5, value5 in value4.items():
                                            if isinstance(value5, str) or isinstance(value5, list):
                                                table.rows.append([item2, item3, item4, item5, value5])

                        if table.rows:
                            print("-" * 100)
                            print(f"Application: `{item2}` validation errors")
                            print("-" * 100)
                            print(table)
                            print()
