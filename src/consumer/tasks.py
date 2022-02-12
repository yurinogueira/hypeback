import time

from django.conf import settings

from celery import shared_task

from consumer.models import Transaction
from consumer.wrappers import Web3ContractWrapper, Web3TokenWrapper


@shared_task
def send_coin_to(nft_id: int):
    nft_wrapper = Web3ContractWrapper()
    nft_w3 = nft_wrapper.connect_to_w3()
    nft_contract = nft_wrapper.get_contract(nft_w3)

    try:
        nft_id_address = nft_contract.functions.ownerOf(nft_id).call()
    except Exception as error:
        print(error)
        return

    token_wrapper = Web3TokenWrapper()
    token_w3 = token_wrapper.connect_to_w3()
    token_contract = token_wrapper.get_contract(token_w3)
    token_account = token_wrapper.get_account(token_w3)

    transaction = Transaction(
        to=nft_id_address,
        value=settings.TOKEN_TRANSFER_AMOUNT,
        web3_connection=token_w3,
        contract=token_contract,
        account=token_account,
    )
    token_wrapper.send_transaction(transaction)


@shared_task
def send_coins():
    for i in range(1, settings.NFT_MAX_AMOUNT + 1, 1):
        send_coin_to.delay(i)
        time.sleep(2)
