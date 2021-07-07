import eth_account

from .utils import waittx

COMMUNITY = "0x378c50D9264C63F3F92B806d4ee56E9D86FfB3Ec"
VALIDATOR_PRIV_KEY = "826E479F5385C8C32CD96B0C0ACCDB8CC4FA5CACCC1BE54C1E3AA4D676A6EFF5"


def test_basic(w3):
    chain_id = w3.eth.chain_id
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
    addr = w3.geth.personal.import_raw_key(VALIDATOR_PRIV_KEY, "1")
    w3.geth.personal.unlock_account(addr, "1")
    assert addr == acct.address, "invalid address"
    print(w3.eth.get_balance(acct.address))
    tx = {
        "from": acct.address,
        "to": COMMUNITY,
        "value": 1000,
        "chainId": chain_id,
        # "gas": 42000,
    }
    txhash = w3.eth.send_transaction(tx)
    print("txhash", txhash.hex())
    tx = waittx(w3, txhash)
    print("get tx", tx)
    print("balance", w3.eth.get_balance(acct.address), w3.eth.getBalance(COMMUNITY))
    print("receipt", w3.eth.get_transaction_receipt(txhash))
    # print("get block", w3.eth.get_block(tx.blockNumber))

    tx = {
        "from": acct.address,
        "to": COMMUNITY,
        "value": 1000,
        "gasPrice": w3.eth.gas_price,
        "nonce": w3.eth.get_transaction_count(acct.address, "pending"),
        "chainId": chain_id,
        # "gas": 42000,
    }
    tx["gas"] = w3.eth.estimate_gas(tx)
    signed = eth_account.Account.sign_transaction(tx, VALIDATOR_PRIV_KEY)
    print("eth tx hash", signed.hash.hex())
    txhash = w3.eth.send_raw_transaction(signed.rawTransaction)
    assert txhash == signed.hash, "invalid tx hash"
    tx = waittx(w3, txhash)
    print("receipt", tx)
