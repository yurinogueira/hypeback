import json

from django.conf import settings
from web3 import Web3
from web3.eth import Contract
from eth_account.account import LocalAccount
from web3.middleware import geth_poa_middleware


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

    def send_transaction(self, to: str, value: int, w3: Web3, ct: Contract, acc: LocalAccount):
        nonce = w3.eth.get_transaction_count(acc.address)
        gas_price = w3.eth.gas_price
        value = value * 1e18
        transaction = ct.functions.transfer(to, int(value)).buildTransaction({
            "gas": 2000000,
            "gasPrice": gas_price,
            "from": acc.address,
            "nonce": nonce,
        })
        private_key = self.account_private_key
        signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)
        transaction = w3.eth.send_raw_transaction(signed_txn.rawTransaction)

        return transaction
