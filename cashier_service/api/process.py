from flask import current_app, Blueprint, jsonify, request
from uuid import uuid4
from json import dumps
from datetime import datetime

process = Blueprint('process', __name__, url_prefix='/cashier/')


@process.route('/create', methods=['POST'])
def process_cashier_requests():
    req_data = request.get_json()
    log = current_app.logger

    operation_id = str(uuid4())
    created = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
    account_number = req_data['accountNumber']
    amount = req_data['amount']
    operation = req_data['operation']

    broker = current_app.broker
    broker.produce(dumps({
        'id': operation_id,
        'accountNumber': account_number,
        'amount': amount,
        'operation': operation,
        'status': 'accepted',
        'created': created
    }))

    return jsonify({
        'id': operation_id,
        'accountNumber': account_number,
        'amount': amount,
        'status': 'accepted',
        'operation': operation,
        'created': created
    }), 202
