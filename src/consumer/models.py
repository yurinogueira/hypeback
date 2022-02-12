from dataclasses import dataclass

from eth_account.account import LocalAccount
from web3 import Web3
from web3.eth import Contract


@dataclass
class Transaction:
    to: str
    value: int
    web3_connection: Web3
    contract: Contract
    account: LocalAccount
