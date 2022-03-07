import json

from django.conf import settings

from eth_account.account import LocalAccount
from web3 import Web3
from web3.eth import Contract
from web3.middleware import geth_poa_middleware
from web3.types import HexBytes, Wei

from consumer.models import Transaction


class Web3ContractWrapper:
    def __init__(self, nft_id: int = 0, abi_file_path: str = "api/static/nft/"):
        self.abi_file_path = abi_file_path
        self.nft_id = nft_id
        self.url = settings.NFTS_URL[nft_id]
        self.contract_address = settings.NFTS_CONTRACT_ADDRESS[nft_id]

    def load_abi(self) -> dict:
        file = open(f"{self.abi_file_path}{self.nft_id}.json")
        data = json.load(file)
        file.close()

        return data

    def connect_to_w3(self) -> Web3:
        provider = Web3.HTTPProvider(self.url, request_kwargs={"timeout": 120})
        w3 = Web3(provider)
        w3.middleware_onion.inject(geth_poa_middleware, layer=0)
        return w3

    def get_contract(self, w3: Web3) -> Contract:
        return w3.eth.contract(self.contract_address, abi=self.load_abi())


class Web3TokenWrapper(Web3ContractWrapper):
    def __init__(self, nft_id: int = 0):
        super(Web3TokenWrapper, self).__init__(nft_id, "api/static/token/")
        self.url = settings.TOKENS_URL[nft_id]
        self.contract_address = settings.TOKENS_CONTRACT_ADDRESS[nft_id]
        self.account_private_key = settings.TOKENS_ACCOUNT_PRIVATE_KEY[nft_id]

    def get_account(self, w3: Web3) -> LocalAccount:
        account = w3.eth.account.from_key(self.account_private_key)
        return account

    def send_transaction(self, transaction_model: Transaction) -> HexBytes:
        to = transaction_model.to
        w3 = transaction_model.web3_connection
        contract = transaction_model.contract
        account = transaction_model.account

        nonce = w3.eth.get_transaction_count(account.address, "pending")
        gas_price = int(w3.eth.gas_price * 1.2)
        value = int(transaction_model.value * 1e18)

        transaction = contract.functions.transfer(to, value).buildTransaction(
            {
                "gas": Wei(20000000),
                "gasPrice": Wei(gas_price),
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
