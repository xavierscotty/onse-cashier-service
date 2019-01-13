import json
from http import HTTPStatus

from behave import when, then


@when(u'I make a request to cashier service')
def make_request(context):
    pass


@when(u'a request json payload')
def request_json_payload(context):
    payload = json.loads(context.text)
    context.response = context.web_client.post('/cashier/create', json=payload)


@then(u'I should receive an "Accepted" response')
def assert_response(context):
    response = context.response
    status_code = response.status_code
    assert status_code == HTTPStatus.ACCEPTED.value, \
        f'Expected status code to be 201; got {status_code}'


@then(u'I should see a "{value}" {key}')
def assert_key_value(context, value, key):
    response = context.response.get_json()
    assert response[key] == value, \
        f'Unexpected JSON; got {repr(response.get_json())} '
