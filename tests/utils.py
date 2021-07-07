import time
from web3.exceptions import TransactionNotFound

ETHERMINT_CHAIN_ID = 1
GETH_CHAIN_ID = 1337


def waittx(w3, txhash, timeout=5):
    expire = time.time() + timeout
    while time.time() < expire:
        try:
            return w3.eth.get_transaction_receipt(txhash)
        except TransactionNotFound:
            pass
        time.sleep(0.5)
    raise TimeoutError(f"get_transaction_receipt timeout {txhash.hex()}")
