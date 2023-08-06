import json

import pytest
from unittest.mock import ANY

from netorca_sdk.exceptions import NetorcaException
from netorca_sdk.netorca import Netorca


def test_get_service_items_no_filters(netorca, auth_mock):
    auth_mock.get.return_value.status_code = 200
    auth_mock.get.return_value.json.return_value = {'results': []}

    result = netorca.get_service_items()

    auth_mock.get.assert_called_once_with(url=ANY, authentication_required=True, filters=None)


def test_get_service_items_error(auth_mock):
    auth_mock.get.return_value.status_code = 500
    auth_mock.get.return_value.json.return_value = {'error': 'Some error'}

    netorca = Netorca(auth=auth_mock)

    with pytest.raises(NetorcaException, match="Could not fetch Service Items due to: {'error': 'Some error'}"):
        netorca.get_service_items()


def test_get_service_items_with_filters(netorca, auth_mock):
    auth_mock.get.return_value.status_code = 200
    auth_mock.get.return_value.json.return_value = {'results': []}
    filters = {'service_name': 'test_service'}

    result = netorca.get_service_items(filters=filters)

    auth_mock.get.assert_called_once_with(url=ANY, authentication_required=True, filters=filters)


def test_get_deployed_items_no_filters(auth_mock):
    auth_mock.get.return_value.status_code = 200
    auth_mock.get.return_value.json.return_value = {'results': []}

    netorca = Netorca(auth=auth_mock)
    result = netorca.get_deployed_items()

    assert result == []
    auth_mock.get.assert_called_once_with(url=ANY, authentication_required=True, filters=None)


def test_get_deployed_items_with_filters(auth_mock):
    auth_mock.get.return_value.status_code = 200
    auth_mock.get.return_value.json.return_value = {'results': []}

    filters = {'some_filter': 'some_value'}

    netorca = Netorca(auth=auth_mock)
    result = netorca.get_deployed_items(filters=filters)

    assert result == []
    auth_mock.get.assert_called_once_with(url=ANY, authentication_required=True, filters=filters)


def test_get_deployed_items_error(auth_mock):
    auth_mock.get.return_value.status_code = 500
    auth_mock.get.return_value.json.return_value = {'error': 'Some error'}

    netorca = Netorca(auth=auth_mock)

    with pytest.raises(NetorcaException, match='Could not fetch Deployed Items due to:'):
        netorca.get_deployed_items()


def test_get_change_instances_no_filters(auth_mock):
    auth_mock.get.return_value.status_code = 200
    auth_mock.get.return_value.json.return_value = {'results': []}

    netorca = Netorca(auth=auth_mock)
    result = netorca.get_change_instances()

    assert result == []
    auth_mock.get.assert_called_once_with(url=ANY, authentication_required=True, filters=None)


def test_get_change_instances_with_filters(auth_mock):
    auth_mock.get.return_value.status_code = 200
    auth_mock.get.return_value.json.return_value = {'results': []}

    filters = {'some_filter': 'some_value'}

    netorca = Netorca(auth=auth_mock)
    result = netorca.get_change_instances(filters=filters)

    assert result == []
    auth_mock.get.assert_called_once_with(url=ANY, authentication_required=True, filters=filters)


def test_get_change_instances_error(auth_mock):
    auth_mock.get.return_value.status_code = 500
    auth_mock.get.return_value.json.return_value = {'error': 'Some error'}

    netorca = Netorca(auth=auth_mock)

    with pytest.raises(NetorcaException, match='Could not fetch Change Instances due to:'):
        netorca.get_change_instances()


def test_create_deployed_item_success(auth_mock):
    change_instance_uuid = '12345678-1234-1234-1234-123456789012'
    data = {'field': 'value'}

    auth_mock.patch.return_value.status_code = 200
    auth_mock.patch.return_value.json.return_value = {'created': True}

    netorca = Netorca(auth=auth_mock)
    result = netorca.create_deployed_item(change_instance_uuid, data)

    assert result == {'created': True}
    auth_mock.patch.assert_called_once_with(
        url=ANY, data=json.dumps({'deployed_item': data}), authentication_required=True
    )


def test_create_deployed_item_error(auth_mock):
    change_instance_uuid = '12345678-1234-1234-1234-123456789012'
    data = {'field': 'value'}

    auth_mock.patch.return_value.status_code = 500
    auth_mock.patch.return_value.json.return_value = {'error': 'Some error'}

    netorca = Netorca(auth=auth_mock)

    with pytest.raises(NetorcaException, match='Could not create deployed item. Log:'):
        netorca.create_deployed_item(change_instance_uuid, data)


def test_update_change_instance_success(auth_mock):
    change_instance_uuid = '12345678-1234-1234-1234-123456789012'
    data = {'field': 'value'}

    auth_mock.patch.return_value.status_code = 200
    auth_mock.patch.return_value.json.return_value = {'updated': True}

    netorca = Netorca(auth=auth_mock)
    result = netorca.update_change_instance(change_instance_uuid, data)

    assert result == {'updated': True}
    auth_mock.patch.assert_called_once_with(
        url=ANY, data=json.dumps(data), authentication_required=True
    )


def test_update_change_instance_error(auth_mock):
    change_instance_uuid = '12345678-1234-1234-1234-123456789012'
    data = {'field': 'value'}

    auth_mock.patch.return_value.status_code = 500
    auth_mock.patch.return_value.json.return_value = {'error': 'Some error'}

    netorca = Netorca(auth=auth_mock)

    with pytest.raises(NetorcaException, match='Could not update change Instance. Log:'):
        netorca.update_change_instance(change_instance_uuid, data)
