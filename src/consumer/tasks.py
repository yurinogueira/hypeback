from django.conf import settings

from celery import shared_task

from consumer.exceptions import NFTNotExistException, TransactionException
from consumer.models import Transaction
from consumer.wrappers import Web3ContractWrapper, Web3TokenWrapper
from notifications.wrappers import SlackWrapper


@shared_task
def send_coin_to(nft_id: int, has_next: bool):
    nft_wrapper = Web3ContractWrapper()
    nft_w3 = nft_wrapper.connect_to_w3()
    nft_contract = nft_wrapper.get_contract(nft_w3)

    try:
        nft_id_address = nft_contract.functions.ownerOf(nft_id).call()
    except Exception as error:
        slack = SlackWrapper()
        message = f"Info: NFT de id {nft_id} não existe." f"```{error}```"
        slack.post_message("#hypeback-log", message)
        raise NFTNotExistException(message)

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
    try:
        token_wrapper.send_transaction(transaction)
    except Exception as error:
        slack = SlackWrapper()
        message = (
            f"Erro: A transação para a carteira {nft_id_address} falhou."
            f"```{error}```"
        )
        slack.post_message("#hypeback-error", message)
        raise TransactionException(message)

    if has_next:
        next_nft_id = nft_id + 1
        next_has_next = next_nft_id < settings.NFT_MAX_AMOUNT
        send_coin_to.apply_async(args=[next_nft_id, next_has_next])


@shared_task
def send_coins():
    send_coin_to.apply_async(args=[1, True])
