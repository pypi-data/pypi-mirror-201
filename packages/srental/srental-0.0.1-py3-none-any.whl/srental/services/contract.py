from typing import List


class Contract:
    def __init__(self, name: str, start: int, duration: int, price: int):
        self.name = name
        self.start = start
        self.duration = duration
        self.price = price

    def __repr__(self):
        return f"Contract(name={self.name}, start={self.start}, duration={self.duration}, price={self.price})"


def parse_contract_json(json_request):
    """
    Parse JSON data for a contract and return a Contract object
    """
    contracts = []
    try:
        for contract_dict in json_request:
            contract = Contract(
                name=contract_dict['name'],
                start=contract_dict['start'],
                duration=contract_dict['duration'],
                price=contract_dict['price']
            )
            contracts.append(contract)
    except Exception as e:
        print(f"Error converting JSON to Contracts: {str(e)}")
    return contracts


def get_optimal_contracts(contracts: List[Contract]) -> (List[Contract], int):
    """
    Given a list of Contract objects, return a list of contracts that maximize profitability
    """

    def calculate_profit(contracts, n, current_profit):
        nonlocal max_profit, result

        if n == len(contracts):
            if current_profit > max_profit:
                max_profit = current_profit
                result = current_solution.copy()
            return

        contract = contracts[n]

        # Skip contract if duration is greater than 24 or overlaps with existing contracts
        if contract.duration > 24 or not is_valid_slot(contract):
            calculate_profit(contracts, n + 1, current_profit)
        else:
            # Include the contract in the solution
            current_solution.append(contract)
            calculate_profit(contracts, n + 1, current_profit + contract.price)
            current_solution.pop()  # Backtrack

        # TODO: Exclude the contract from the solution
        calculate_profit(contracts, n + 1, current_profit)

    def is_valid_slot(contract):
        for c in current_solution:
            if contract.start < c.start + c.duration and contract.start + contract.duration > c.start:
                return False
        return True

    max_profit = 0
    result = []
    current_solution = []

    calculate_profit(contracts, 0, 0)

    return result, max_profit
