import eth_account

from .utils import ADDRS, KEYS, waittx


def test_genesis_status(w3):
    assert (
        w3.eth.get_balance(ADDRS["validator"]) == 1000000000000000000
    ), "invalid genesis state"
    assert (
        w3.eth.get_balance(ADDRS["community"]) == 10000000000000000000000
    ), "invalid genesis state"


def test_basic(w3):
    chain_id = w3.eth.chain_id
    print(
        "test estimated gas",
        w3.eth.estimate_gas(
            {
                "to": "0x11f4d0A3c12e86B4b5F39B213F7E19D048276DAe",
                "data": "0xc6888fa10000000000000000000000000000000000000000000000000000000000000003",
            }
        ),
    )

    acct = eth_account.Account.from_key(KEYS["validator"])
    tx = {
        "from": acct.address,
        "to": ADDRS["community"],
        "value": 1000,
        "chainId": chain_id,
    }
    assert w3.eth.estimate_gas(tx) == 21000, "invalid gas amount"
    txhash = w3.eth.send_transaction(tx)
    tx = w3.eth.get_transaction(txhash)
    tx = waittx(w3, txhash)
    print("get tx", tx)
    print(
        "balance",
        w3.eth.get_balance(acct.address),
        w3.eth.get_balance(ADDRS["community"]),
    )
    print("receipt", w3.eth.get_transaction_receipt(txhash))
    # print("get block", w3.eth.get_block(tx.blockNumber))

    tx = {
        "from": acct.address,
        "to": ADDRS["community"],
        "value": 1000,
        "gasPrice": w3.eth.gas_price,
        "nonce": w3.eth.get_transaction_count(acct.address, "pending"),
        "chainId": chain_id,
        # "gas": 42000,
    }
    tx["gas"] = w3.eth.estimate_gas(tx)
    signed = eth_account.Account.sign_transaction(tx, KEYS["validator"])
    print("eth tx hash", signed.hash.hex())
    txhash = w3.eth.send_raw_transaction(signed.rawTransaction)
    assert txhash == signed.hash, "invalid tx hash"
    tx = waittx(w3, txhash)
    print("receipt", tx)
