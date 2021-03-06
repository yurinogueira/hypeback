from django.conf import settings

from celery import shared_task

from consumer.exceptions import NFTNotExistException, TransactionException
from consumer.models import Transaction
from consumer.wrappers import Web3ContractWrapper, Web3TokenWrapper
from notifications.wrappers import SlackWrapper


@shared_task
def send_coin_to(nft_id: int, has_next: bool, nft: int, token: int):
    nft_wrapper = Web3ContractWrapper(nft)
    nft_w3 = nft_wrapper.connect_to_w3()
    nft_contract = nft_wrapper.get_contract(nft_w3)

    try:
        nft_id_address = nft_contract.functions.ownerOf(nft_id).call()
    except Exception as error:
        slack = SlackWrapper()
        message = f"Info: NFT de id {nft_id} não existe." f"```{error}```"
        slack.post_message("#hypeback-log", message)
        raise NFTNotExistException(message)

    token_wrapper = Web3TokenWrapper(token)
    token_w3 = token_wrapper.connect_to_w3()
    token_contract = token_wrapper.get_contract(token_w3)
    token_account = token_wrapper.get_account(token_w3)

    transaction = Transaction(
        to=nft_id_address,
        value=int(settings.TOKENS_TRANSFER_AMOUNT[0]),
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
        next_has_next = next_nft_id < int(settings.NFTS_MAX_AMOUNT[nft])
        send_coin_to.apply_async(args=[next_nft_id, next_has_next])


@shared_task
def send_coin_to_list(nft_list_id: list[int], index: int, nft: int, token: int):
    send_coin_to(nft_list_id[index], False, nft, token)
    index += 1
    if index < len(nft_list_id):
        send_coin_to_list.apply_async(args=[nft_list_id, index, nft, token])


@shared_task
def send_coins(nft: int, token: int):
    send_coin_to.apply_async(args=[1, True, nft, token])
