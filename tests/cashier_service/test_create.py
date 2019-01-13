import json
from unittest.mock import Mock

import pytest

from cashier_service.app import create
from cashier_service.mock.mock_events import MockEvents
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
    return MockEvents()


def test_should_produce_event(web_client, logger, broker):
    payload = dict(accountNumber='12345678', amount=10815, operation='debit')

    web_client.post('/cashier/create', json=json.loads(json.dumps(payload)))

    event = json.loads(broker.last_event)

    assert event is not None
    assert 'id' in event
    assert event['accountNumber'] == '12345678'
    assert event['amount'] == 10815
    assert event['operation'] == 'debit'
    assert event['status'] == 'accepted'
    assert 'created' in event


def test_should_process_client_request(web_client):
    payload = dict(accountNumber="12345678", amount=10815, operation="credit")

    response = web_client.post('/cashier/create',
                               json=json.loads(json.dumps(payload)))
    assert response.status_code == 202, response.status_code
    assert response.is_json
    assert response.get_json()['accountNumber'] == '12345678', \
        f'Unexpected JSON; got {repr(response.get_json())}'


def test_bad_content_type(web_client):
    response = web_client.post('/cashier/create', data='not json')

    assert response.status_code == 415, response.status_code


@pytest.mark.parametrize(
    'payload',
    [dict(),
     dict(acountNumber='12345678', amount=1, operation='credit', x='?'),
     dict(acountNumber='12345678', amount=0, operation='credit'),
     dict(acountNumber='12345678', amount=1, operation='unknown'),
     dict(acountNumber='12345678', amount='1', operation='credit'),
     dict(acountNumber='1234567', amount='1', operation='credit'),
     dict(acountNumber='123456789', amount='1', operation='credit')])
def test_bad_payloads(payload, web_client):
    response = web_client.post('/cashier/create', json=payload)

    assert response.status_code == 400, response.status_code
