import time

import eth_account
import web3
from web3.exceptions import TransactionNotFound

COMMUNITY = "0x378c50D9264C63F3F92B806d4ee56E9D86FfB3Ec"
VALIDATOR_PRIV_KEY = "826E479F5385C8C32CD96B0C0ACCDB8CC4FA5CACCC1BE54C1E3AA4D676A6EFF5"
CHAIN_ID = 1


def waittx(w3, txhash, timeout=5):
    expire = time.time() + timeout
    while time.time() < expire:
        try:
            return w3.eth.getTransactionReceipt(txhash)
        except TransactionNotFound:
            pass
        time.sleep(0.5)
    raise TimeoutError(f"getTransactionReceipt timeout {txhash.hex()}")


def test_basic(ethermint):
    w3 = web3.Web3(web3.providers.HTTPProvider("http://localhost:1317"))
    # print(
    #     "test estimated gas",
    #     w3.eth.estimateGas(
    #         {
    #             "to": "0x11f4d0A3c12e86B4b5F39B213F7E19D048276DAe",
    #             "data": "0xc6888fa10000000000000000000000000000000000000000000000000000000000000003",
    #         }
    #     ),
    # )

    acct = eth_account.Account.from_key(VALIDATOR_PRIV_KEY)
    addr = w3.geth.personal.importRawKey(VALIDATOR_PRIV_KEY, "1")
    assert addr == acct.address, "invalid address"
    print(w3.eth.getBalance(acct.address))
    tx = {
        "from": acct.address,
        "to": COMMUNITY,
        "value": 1000,
        "chainId": CHAIN_ID,
        # "gas": 42000,
    }
    txhash = w3.eth.sendTransaction(tx)
    print("txhash", txhash.hex())
    tx = waittx(w3, txhash)
    print("get tx", tx)
    print("balance", w3.eth.getBalance(acct.address), w3.eth.getBalance(COMMUNITY))
    print("receipt", w3.eth.getTransactionReceipt(txhash))
    # print("get block", w3.eth.get_block(tx.blockNumber))

    tx = {
        "from": acct.address,
        "to": COMMUNITY,
        "value": 1000,
        "gasPrice": w3.eth.gasPrice,
        "nonce": w3.eth.getTransactionCount(acct.address, "pending"),
        "chainId": CHAIN_ID,
        # "gas": 42000,
    }
    tx["gas"] = w3.eth.estimateGas(tx)
    signed = eth_account.Account.sign_transaction(tx, VALIDATOR_PRIV_KEY)
    print("eth tx hash", signed.hash.hex())
    txhash = w3.eth.sendRawTransaction(signed.rawTransaction)
    assert txhash == signed.hash, 'invalid tx hash'
    tx = waittx(w3, txhash)
    print("receipt", tx)
