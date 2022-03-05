import json

import pytest
from web3 import EthereumTesterProvider, Web3


class TestWeb3Contract:
    @pytest.fixture
    def tester_provider(self):
        return EthereumTesterProvider()

    @pytest.fixture
    def eth_tester(self, tester_provider):
        return tester_provider.ethereum_tester

    @pytest.fixture
    def w3(self, tester_provider):
        return Web3(tester_provider)

    @pytest.fixture
    def bytecode(self):
        with open("api/static/nft/test.txt") as file:
            return file.readline()

    @pytest.fixture
    def abi(self):
        with open("api/static/nft/test.json") as file:
            return json.load(file)

    @pytest.fixture
    def contract_tester(self, eth_tester, w3, bytecode, abi):
        deploy_address = eth_tester.get_accounts()[0]
        contract = w3.eth.contract(abi=abi, bytecode=bytecode)

        tx_hash = contract.constructor().transact({"from": deploy_address})
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash, 180)

        return contract(tx_receipt.contractAddress)

    def test_total_supply(self, contract_tester):
        total_supply = contract_tester.caller.totalSupply()
        expected_supply = 1000000 * (10 ** contract_tester.caller.decimals())

        assert expected_supply == total_supply

    def test_token_symbol(self, contract_tester):
        symbol = contract_tester.caller.symbol()
        expected_symbol = "GTN"

        assert expected_symbol == symbol

    def test_token_name(self, contract_tester):
        name = contract_tester.caller.name()
        expected_name = "GATUNO"

        assert expected_name == name
