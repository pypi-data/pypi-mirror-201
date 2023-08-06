import unittest

from srental.services import Contract, get_optimal_contracts, parse_contract_json


class TestContractService(unittest.TestCase):

    def test_empty_contract(self):
        # Given
        expected_result = []
        expected_profit = 0

        # When
        optimal_contracts, max_profit = get_optimal_contracts([])

        # Then
        self.assertEqual(optimal_contracts, expected_result)
        self.assertEqual(max_profit, expected_profit)

    def test_single_contract(self):
        # Given
        contract1 = Contract("Contract1", 0, 5, 10)
        expected_result = [contract1]
        expected_profit = 10

        # When
        optimal_contracts, max_profit = get_optimal_contracts([contract1])

        # Then
        self.assertEqual(optimal_contracts, expected_result)
        self.assertEqual(max_profit, expected_profit)

    def test_multiple_contract_with_different_durations(self):
        # Given
        contract1 = Contract("Contract1", 0, 5, 10)
        contract2 = Contract("Contract2", 7, 8, 14)
        contract3 = Contract("Contract3", 15, 6, 8)
        contracts = [contract1, contract2, contract3]
        expected_result = [contract1, contract2, contract3]
        expected_profit = 32

        # When
        optimal_contracts, max_profit = get_optimal_contracts(contracts)
        # Then
        self.assertEqual(optimal_contracts, expected_result)
        self.assertEqual(max_profit, expected_profit)

    def test_multiple_contract_with_larger_duration(self):
        # Given
        contract1 = Contract("Contract1", 15, 25, 30)
        contract2 = Contract("Contract2", 20, 26, 28)
        contracts = [contract1, contract2]
        expected_result = []
        expected_profit = 0

        # When
        optimal_contracts, max_profit = get_optimal_contracts(contracts)
        # Then
        self.assertEqual(optimal_contracts, expected_result)
        self.assertEqual(max_profit, expected_profit)

    def test_multiple_contract_with_negative_prices(self):
        # Given
        contract1 = Contract("Contract1", 2, 10, -5)
        contract2 = Contract("Contract2", 5, 6, -8)
        contracts = [contract1, contract2]
        expected_result = []
        expected_profit = 0

        # When
        optimal_contracts, max_profit = get_optimal_contracts(contracts)
        # Then
        self.assertEqual(optimal_contracts, expected_result)
        self.assertEqual(max_profit, expected_profit)

    def test_multiple_contract_with_overlaps(self):
        # Given
        contract1 = Contract("Contract1", 0, 5, 10)
        contract2 = Contract("Contract2", 3, 7, 14)
        contract3 = Contract("Contract3", 5, 9, 8)
        contract4 = Contract("Contract4", 5, 9, 7)

        expected_result = [contract1, contract3]
        expected_profit = 18

        # When
        contracts = [contract1, contract2, contract3, contract4]
        optimal_contracts, max_profit = get_optimal_contracts(contracts)

        # Then
        self.assertEqual(optimal_contracts, expected_result)
        self.assertEqual(max_profit, expected_profit)

    def test_multiple_contract_with_complex_combinations(self):
        # Given
        contract1 = Contract("Contract1", 0, 5, 10)
        contract2 = Contract("Contract2", 1, 6, 14)
        contract3 = Contract("Contract3", 5, 8, 10)
        contract4 = Contract("Contract4", 7, 9, 20)
        contract5 = Contract("Contract5", 18, 6, 30)
        contract6 = Contract("Contract5", 13, 4, 6)

        expected_result = [contract2, contract4, contract5]
        expected_profit = 64

        # When
        contracts = [contract1, contract2, contract3, contract4, contract5, contract6]
        optimal_contracts, max_profit = get_optimal_contracts(contracts)

        # Then
        self.assertEqual(optimal_contracts, expected_result)
        self.assertEqual(max_profit, expected_profit)


if __name__ == '__main__':
    unittest.main()
