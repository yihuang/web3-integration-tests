from .utils import ADDRS, contract_address, waittx


def test_account_override(w3):
    owner = ADDRS["validator"]
    nonce = w3.eth.get_transaction_count(owner, "pending")
    next_contract_addr = contract_address(owner, nonce + 1)
    txhash = w3.eth.send_transaction(
        {"from": owner, "to": next_contract_addr, "value": 1000}
    )
    waittx(w3, txhash)
    assert w3.eth.get_balance(next_contract_addr) == 1000, "invalid balance"

    # deploy a random contract
    from .test_erc20 import abi, bytecode

    erc20_contract = w3.eth.contract(abi=abi, bytecode=bytecode)
    txhash = erc20_contract.constructor().transact({"from": owner})
    receipt = waittx(w3, txhash)
    assert receipt.contractAddress == next_contract_addr, "wrong contract address"
    assert w3.eth.get_balance(next_contract_addr) == 1000, "invalid balance"
