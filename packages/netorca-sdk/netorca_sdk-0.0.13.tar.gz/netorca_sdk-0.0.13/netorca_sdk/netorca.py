import json

from netorca_sdk.auth import AbstractNetorcaAuth
from netorca_sdk.config import SERVICE_ITEMS_ENDPOINT, DEPLOYED_ITEMS_ENDPOINT, CHANGE_INSTANCES_ENDPOINT, \
    SERVICE_CONFIG_ENDPOINT, logger
from netorca_sdk.exceptions import NetorcaException


class Netorca:
    def __init__(self, auth: AbstractNetorcaAuth):
        self.auth = auth

    def get_service_items(self, filters=None):
        """
        Fetches service items from the Netorca API based on the provided filters.

        :param filters: Optional dictionary containing filters to apply to the API request.
                        Example format: {"service_name": "my_service"}
        :type filters: dict, optional

        :return: A list of service items matching the provided filters.
        :rtype: list

        :raises NetorcaException: If the API request fails or encounters an error.
        """
        logger.info(f"Fetching service items with filters: {filters}")

        SERVICE_ITEMS_URL = f"{self.auth.fqdn}{SERVICE_ITEMS_ENDPOINT}"
        response = self.auth.get(url=SERVICE_ITEMS_URL, authentication_required=True, filters=filters)
        if response.status_code == 200:
            return response.json()['results']

        logger.error(f"Could not fetch Service Items due to: {response.json()}")
        raise NetorcaException(f"Could not fetch Service Items due to: {response.json()}")

    def get_deployed_items(self, filters=None):
        """
        Fetches deployed items from the Netorca API based on the provided filters.

        :param filters: Optional dictionary containing filters to apply to the API request.
        :type filters: dict, optional

        :return: A list of deployed items matching the provided filters.
        :rtype: list

        :raises NetorcaException: If the API request fails or encounters an error.
        """
        logger.info(f"Fetching deployed items with filters: {filters}")

        DEPLOYED_ITEMS_URL = f"{self.auth.fqdn}{DEPLOYED_ITEMS_ENDPOINT}"
        response = self.auth.get(url=DEPLOYED_ITEMS_URL, authentication_required=True, filters=filters)
        if response.status_code == 200:
            return response.json()['results']

        logger.error(f"Could not fetch Deployed Items due to: {response.json()}")
        raise NetorcaException(f"Could not fetch Deployed Items due to: {response.json()}")

    def get_change_instances(self, filters=None):
        """
        Fetches change instances from the Netorca API based on the provided filters.

        :param filters: Optional dictionary containing filters to apply to the API request.
                        Example format: {"service_name": "my_service1,my_service2"}
        :type filters: dict, optional

        :return: A list of change instances matching the provided filters.
        :rtype: list

        :raises NetorcaException: If the API request fails or encounters an error.
        """
        logger.info(f"Fetching change instances with filters: {filters}")

        CHANGE_INSTANCES_URL = f"{self.auth.fqdn}{CHANGE_INSTANCES_ENDPOINT}"
        response = self.auth.get(url=CHANGE_INSTANCES_URL, authentication_required=True, filters=filters)
        if response.status_code == 200:
            return response.json()['results']

        logger.error(f"Could not fetch Change Instances due to: {response.json()}")
        raise NetorcaException(f"Could not fetch Change Instances due to: {response.json()}")

    def create_deployed_item(self, change_instance_uuid: str, data: dict):
        """
        Creates a Deployed Item for a specified Change Instance in the Netorca API.

        :param change_instance_uuid: UUID of the ChangeInstance to which the DeployedItem should be added.
        :type change_instance_uuid: str

        :param data: Dictionary containing the metadata of the DeployedItem to be created.
                     Example format: {"key": "value"}
        :type data: dict

        :return: A dictionary containing the updated ChangeInstance with the new DeployedItem.
        :rtype: dict

        :raises NetorcaException: If the API request fails or encounters an error.
        """
        logger.info(f"Creating deployed item for change_instance_uuid: {change_instance_uuid} with data: {data}")

        CHANGE_INSTANCES_URL = f"{self.auth.fqdn}{CHANGE_INSTANCES_ENDPOINT}{change_instance_uuid}/"
        data = {
            'deployed_item': data
        }
        response = self.auth.patch(url=CHANGE_INSTANCES_URL, data=json.dumps(data), authentication_required=True)
        if response.status_code == 200:
            return response.json()

        logger.error(f"Could not create deployed item. Log: {response.json()}")
        raise NetorcaException(f"Could not create deployed item. Log: {response.json()}")

    def update_change_instance(self, change_instance_uuid, data):
        """
        Update a Deployed Item for a specified Change Instance in the Netorca API.

        :param change_instance_uuid: UUID of the ChangeInstance to which the DeployedItem should be added.
        :type change_instance_uuid: str

        :param data: Dictionary containing the metadata of the DeployedItem to be created.
                     Example format: {"key": "value"}
        :type data: dict

        :return: A dictionary containing the updated ChangeInstance with the new DeployedItem.
        :rtype: dict

        :raises NetorcaException: If the API request fails or encounters an error.
        """
        logger.info(f"Updating change instance with UUID: {change_instance_uuid} and data: {data}")

        CHANGE_INSTANCES_URL = f"{self.auth.fqdn}{CHANGE_INSTANCES_ENDPOINT}{change_instance_uuid}/"
        response = self.auth.patch(url=CHANGE_INSTANCES_URL, data=json.dumps(data), authentication_required=True)
        if response.status_code == 200:
            return response.json()

        logger.error(f"Could not update Change Instance. Log: {response.json()}")
        raise NetorcaException(f"Could not update change Instance. Log: {response.json()}")

    def get_service_config(self, config_uuid=None, filters=None):
        """
        Fetches service configuration(s) from the Netorca API based on the provided config_uuid or filters.

        :param config_uuid: Optional UUID of the specific service configuration to fetch.
                            If provided, filters will be ignored.
        :type config_uuid: str, optional

        :param filters: Optional dictionary containing filters to apply to the API request.
                        Example format: {"config_name": "PR019_IIW_001_config"}
                        Ignored if config_uuid is provided.
        :type filters: dict, optional

        :return: A dictionary containing the service configuration(s) matching the provided config_uuid or filters.
                 If config_uuid is provided, a single configuration will be returned; otherwise, a list of configurations.
        :rtype: dict or list

        :raises NetorcaException: If the API request fails or encounters an error.
        """
        logger.info(f"Fetching service config with config_uuid: {config_uuid} and filters: {filters}")

        SERVICE_CONFIG_URL = f"{self.auth.fqdn}{SERVICE_CONFIG_ENDPOINT}"
        if config_uuid:
            SERVICE_CONFIG_URL = f"{self.auth.fqdn}{SERVICE_CONFIG_ENDPOINT}{config_uuid}"

        response = self.auth.get(url=SERVICE_CONFIG_URL, authentication_required=True, filters=filters)
        if response.status_code == 200:
            return response.json()
        logger.error(f"Could not get service config. Log: {response.json()}")
        raise NetorcaException(f"Could not get service config. Log: {response.json()}")
