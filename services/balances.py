from typing import Optional, Union

import requests
from eth_typing import Address, ChecksumAddress
from web3 import Web3

from config import COINGECKO_API_URL, ETHEREUM_RPC_URL, CURVE_CONTRACT_ADDRESS, CURVE_CONTRACT_ABI, VS_CURRENCY

web3 = Web3(Web3.HTTPProvider(ETHEREUM_RPC_URL))


def get_token_balance(wallet_address: Optional[Union[Address, ChecksumAddress]]):
    contract = web3.eth.contract(address=CURVE_CONTRACT_ADDRESS, abi=CURVE_CONTRACT_ABI)

    wallet_address = web3.to_checksum_address(wallet_address)

    balance = contract.functions.balanceOf(wallet_address).call()
    decimals = contract.functions.decimals().call()
    readable_token_balance = balance / 10 ** decimals

    return readable_token_balance


def get_price(contract_address: Address, vs_currency: str):
    url = f"{COINGECKO_API_URL}/simple/token_price/ethereum" \
          f"?contract_addresses={contract_address}&vs_currencies={vs_currency}"
    response = requests.get(url=url)
    price = response.json()[contract_address.lower()][vs_currency]
    return price


def get_balances(wallet_address: Optional[Union[Address, ChecksumAddress]]):
    token_balance = get_token_balance(wallet_address)

    usd_price = get_price(CURVE_CONTRACT_ADDRESS, VS_CURRENCY)
    usd_balance = usd_price * token_balance
    return token_balance, usd_balance
