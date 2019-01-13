import json
from unittest.mock import Mock

import pytest

from cashier_service.app import create
from cashier_service.settings import config


@pytest.fixture(scope='function')
def web_client(logger, broker):
    return create(config=config['testing'],
                  broker=broker,
                  logger=logger).test_client()


@pytest.fixture(scope='function')
def logger():
    return Mock()


@pytest.fixture(scope='function')
def broker():
    return Mock()


def test_should_produce_event(web_client, logger, broker):
    payload = {
        "accountNumber": "some-acc-number",
        "amount": 10815,
        "operation": "debit"
    }
    web_client.post('/cashier/create', json=json.loads(json.dumps(payload)))
    broker.produce.assert_called_once()


def test_should_process_client_request(web_client):
    payload = {
        "accountNumber": "some-acc-number",
        "amount": 10815,
        "operation": "credit"
    }
    response = web_client.post('/cashier/create',
                               json=json.loads(json.dumps(payload)))
    assert response.status_code == 202, response.status_code
    assert response.is_json
    assert response.get_json()['accountNumber'] == 'some-acc-number', \
        f'Unexpected JSON; got {repr(response.get_json())}'
