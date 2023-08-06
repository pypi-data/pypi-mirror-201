import logging

from flask import jsonify, request
from . import app
from ..services.contract import parse_contract_json, get_optimal_contracts

logger = logging.getLogger(__name__)


@app.route('/spaceship/optimize', methods=['POST'])
def optimize_spaceship():
    request_data = request.get_json()
    logger.info("Received spaceship optimize request!")
    contracts = parse_contract_json(request_data)
    optimal_contracts, max_profit = get_optimal_contracts(contracts)
    optimal_contract_names = [contract.name for contract in optimal_contracts]
    return jsonify({'income': max_profit, 'path': optimal_contract_names})


# default route
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def catch_all(path):
    return 'Endpoint not found, Currently only support:/spaceship/optimize', 404
