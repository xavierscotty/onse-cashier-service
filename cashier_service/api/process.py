from flask import current_app, Blueprint, jsonify, request
from uuid import uuid4
from json import dumps

process = Blueprint('process', __name__, url_prefix='/cashier/')


@process.route('/create', methods=['POST'])
def process_cashier_requests():
    req_data = request.get_json()
    log = current_app.logger

    operation_id = str(uuid4())
    account_name = req_data['accountNumber']
    amount = req_data['amount']
    action = req_data['action']

    broker = current_app.broker
    broker.produce(dumps({
        'id': operation_id,
        'accountNumber': account_name,
        'amount': amount,
        'action': action
    }))

    return jsonify({
        'id': operation_id,
        'accountNumber': account_name,
        'amount': amount,
        'status': 'pending',
        'action': action
    }), 201
