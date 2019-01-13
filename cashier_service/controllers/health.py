from flask import Blueprint, jsonify

health = Blueprint('health', __name__, url_prefix='/cashier/')


@health.route('/health')
def get_health():
    return jsonify(message='OK')
