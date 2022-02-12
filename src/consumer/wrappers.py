import json

from django.conf import settings

from eth_account.account import LocalAccount
from web3 import Web3
from web3.eth import Contract
from web3.middleware import geth_poa_middleware
from web3.types import HexBytes, Wei

from consumer.models import Transaction


class Web3ContractWrapper:
    def __init__(self):
        self.api_key = settings.GET_BLOCK_API_KEY
        self.url = settings.GET_BLOCK_URL
        self.contract_address = settings.CONTRACT_ADDRESS
        self.abi_file_name = settings.ABI_FILE_NAME
        self.account_private_key = settings.ACCOUNT_PRIVATE_KEY
        self.chain_id = settings.CHAIN_ID

    def load_abi(self) -> dict:
        file = open(self.abi_file_name)
        data = json.load(file)
        file.close()

        return data

    def connect_to_w3(self) -> Web3:
        provider = Web3.HTTPProvider(f"{self.url}{self.api_key}")
        w3 = Web3(provider)
        w3.middleware_onion.inject(geth_poa_middleware, layer=0)
        return w3

    def get_contract(self, w3: Web3) -> Contract:
        abi = self.load_abi()
        contract = w3.eth.contract(abi=abi, address=self.contract_address)
        return contract

    def get_account(self, w3: Web3) -> LocalAccount:
        account = w3.eth.account.from_key(self.account_private_key)
        return account

    def send_transaction(self, transaction_model: Transaction) -> HexBytes:
        to = transaction_model.to
        w3 = transaction_model.web3_connection
        contract = transaction_model.contract
        account = transaction_model.account

        nonce = w3.eth.get_transaction_count(account.address)
        gas_price = w3.eth.gas_price
        value = int(transaction_model.value * 1e18)

        transaction = contract.functions.transfer(to, value).buildTransaction(
            {
                "gas": Wei(2000000),
                "gasPrice": gas_price,
                "from": account.address,
                "nonce": nonce,
            }
        )
        private_key = self.account_private_key
        signed_txn = w3.eth.account.sign_transaction(
            transaction_dict=transaction, private_key=private_key
        )
        result = w3.eth.send_raw_transaction(signed_txn.rawTransaction)

        return result
