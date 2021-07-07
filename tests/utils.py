import time
from web3.exceptions import TransactionNotFound

ETHERMINT_CHAIN_ID = 1
GETH_CHAIN_ID = 1337
VALIDATOR_PRIV_KEY = "826E479F5385C8C32CD96B0C0ACCDB8CC4FA5CACCC1BE54C1E3AA4D676A6EFF5"
COMMUNITY = "0x378c50D9264C63F3F92B806d4ee56E9D86FfB3Ec"


def waittx(w3, txhash, timeout=5):
    expire = time.time() + timeout
    while time.time() < expire:
        try:
            return w3.eth.get_transaction_receipt(txhash)
        except TransactionNotFound:
            pass
        time.sleep(0.5)
    raise TimeoutError(f"get_transaction_receipt timeout {txhash.hex()}")
