import time

import eth_account
import eth_utils
import rlp
from web3.exceptions import TransactionNotFound

ETHERMINT_CHAIN_ID = 1
GETH_CHAIN_ID = 1337
KEYS = {
    "validator": "826E479F5385C8C32CD96B0C0ACCDB8CC4FA5CACCC1BE54C1E3AA4D676A6EFF5",
    "community": "5D665FBD2FB40CB8E9849263B04457BA46D5F948972D0FE4C1F19B6B0F243574",
}
ADDRS = {name: eth_account.Account.from_key(key).address for name, key in KEYS.items()}


def waittx(w3, txhash, timeout=5):
    expire = time.time() + timeout
    while time.time() < expire:
        try:
            return w3.eth.get_transaction_receipt(txhash)
        except TransactionNotFound:
            pass
        time.sleep(0.5)
    raise TimeoutError(f"get_transaction_receipt timeout {txhash.hex()}")


class ContractAddress(rlp.Serializable):
    fields = [
        ("from", rlp.sedes.Binary()),
        ("nonce", rlp.sedes.big_endian_int),
    ]


def contract_address(addr, nonce):
    return eth_utils.to_checksum_address(
        eth_utils.to_hex(
            eth_utils.keccak(
                rlp.encode(ContractAddress(eth_utils.to_bytes(hexstr=addr), nonce))
            )[12:]
        )
    )
