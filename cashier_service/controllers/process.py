from datetime import datetime
from json import dumps
from uuid import uuid4

from flask import current_app, Blueprint, jsonify, request, send_from_directory

from cashier_service import get_app_base_path

process = Blueprint('process', __name__, url_prefix='/cashier/')


@process.route('/create', methods=['POST'])
def process_cashier_requests():
    req_data = request.get_json()

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


@process.route('/swagger.yml', methods=['GET'])
def get_swagger():
    return send_from_directory(get_app_base_path(), 'swagger.yml')
