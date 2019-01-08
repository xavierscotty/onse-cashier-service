import json
@when(u'I make a request to cashier service')
def step_impl(context):
    pass

@when(u'a request json payload')
def step_impl(context):
    payload = json.loads(context.text)
    context.response = context.web_client.post('/cashier/create', json = payload)

@then(u'I should receive a CREATED response')
def step_impl(context):
    response = context.response
    status_code = response.status_code
    assert status_code == 201, f'Expected status code to be 201; got {status_code}'


@then(u'I should see a {value} {key}')
def step_impl(context, key, value):
    response = context.response.get_json()
    assert response[key] == value, f'Unexpected JSON; got {repr(response.get_json())} '
