import json

import eth_account
import eth_utils
import pytest
import rlp

from .utils import ADDRS, KEYS, contract_address, waittx

bytecode = "60806040523480156200001157600080fd5b506040805190810160405280600381526020017f514b430000000000000000000000000000000000000000000000000000000000815250600090805190602001906200005f929190620001af565b506040805190810160405280600d81526020017f5175696b4e6f646520436f696e0000000000000000000000000000000000000081525060019080519060200190620000ad929190620001af565b5060028060006101000a81548160ff021916908360ff160217905550620186a0600381905550600354600460007357f96e6b86cdefdb3d412547816a82e3e0ebf9d273ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020819055507357f96e6b86cdefdb3d412547816a82e3e0ebf9d273ffffffffffffffffffffffffffffffffffffffff16600073ffffffffffffffffffffffffffffffffffffffff167fddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef6003546040518082815260200191505060405180910390a36200025e565b828054600181600116156101000203166002900490600052602060002090601f016020900481019282601f10620001f257805160ff191683800117855562000223565b8280016001018555821562000223579182015b828111156200022257825182559160200191906001019062000205565b5b50905062000232919062000236565b5090565b6200025b91905b80821115620002575760008160009055506001016200023d565b5090565b90565b6110fe806200026e6000396000f3006080604052600436106100db576000357c0100000000000000000000000000000000000000000000000000000000900463ffffffff16806306fdde03146100e0578063095ea7b31461017057806318160ddd146101d557806323b872dd14610200578063313ce567146102855780633eaaf86b146102b657806370a08231146102e157806395d89b4114610338578063a293d1e8146103c8578063a9059cbb14610413578063b5931f7c14610478578063cae9ca51146104c3578063d05c78da1461056e578063dd62ed3e146105b9578063e6cb901314610630575b600080fd5b3480156100ec57600080fd5b506100f561067b565b6040518080602001828103825283818151815260200191508051906020019080838360005b8381101561013557808201518184015260208101905061011a565b50505050905090810190601f1680156101625780820380516001836020036101000a031916815260200191505b509250505060405180910390f35b34801561017c57600080fd5b506101bb600480360381019080803573ffffffffffffffffffffffffffffffffffffffff16906020019092919080359060200190929190505050610719565b604051808215151515815260200191505060405180910390f35b3480156101e157600080fd5b506101ea61080b565b6040518082815260200191505060405180910390f35b34801561020c57600080fd5b5061026b600480360381019080803573ffffffffffffffffffffffffffffffffffffffff169060200190929190803573ffffffffffffffffffffffffffffffffffffffff16906020019092919080359060200190929190505050610856565b604051808215151515815260200191505060405180910390f35b34801561029157600080fd5b5061029a610ae6565b604051808260ff1660ff16815260200191505060405180910390f35b3480156102c257600080fd5b506102cb610af9565b6040518082815260200191505060405180910390f35b3480156102ed57600080fd5b50610322600480360381019080803573ffffffffffffffffffffffffffffffffffffffff169060200190929190505050610aff565b6040518082815260200191505060405180910390f35b34801561034457600080fd5b5061034d610b48565b6040518080602001828103825283818151815260200191508051906020019080838360005b8381101561038d578082015181840152602081019050610372565b50505050905090810190601f1680156103ba5780820380516001836020036101000a031916815260200191505b509250505060405180910390f35b3480156103d457600080fd5b506103fd6004803603810190808035906020019092919080359060200190929190505050610be6565b6040518082815260200191505060405180910390f35b34801561041f57600080fd5b5061045e600480360381019080803573ffffffffffffffffffffffffffffffffffffffff16906020019092919080359060200190929190505050610c02565b604051808215151515815260200191505060405180910390f35b34801561048457600080fd5b506104ad6004803603810190808035906020019092919080359060200190929190505050610d8b565b6040518082815260200191505060405180910390f35b3480156104cf57600080fd5b50610554600480360381019080803573ffffffffffffffffffffffffffffffffffffffff16906020019092919080359060200190929190803590602001908201803590602001908080601f0160208091040260200160405190810160405280939291908181526020018383808284378201915050505050509192919290505050610daf565b604051808215151515815260200191505060405180910390f35b34801561057a57600080fd5b506105a36004803603810190808035906020019092919080359060200190929190505050610ffe565b6040518082815260200191505060405180910390f35b3480156105c557600080fd5b5061061a600480360381019080803573ffffffffffffffffffffffffffffffffffffffff169060200190929190803573ffffffffffffffffffffffffffffffffffffffff16906020019092919050505061102f565b6040518082815260200191505060405180910390f35b34801561063c57600080fd5b5061066560048036038101908080359060200190929190803590602001909291905050506110b6565b6040518082815260200191505060405180910390f35b60018054600181600116156101000203166002900480601f0160208091040260200160405190810160405280929190818152602001828054600181600116156101000203166002900480156107115780601f106106e657610100808354040283529160200191610711565b820191906000526020600020905b8154815290600101906020018083116106f457829003601f168201915b505050505081565b600081600560003373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060008573ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020819055508273ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff167f8c5be1e5ebec7d5bd14f71427d1e84f3dd0314c0f7b2291e5b200ac8c7c3b925846040518082815260200191505060405180910390a36001905092915050565b6000600460008073ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020019081526020016000205460035403905090565b60006108a1600460008673ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020019081526020016000205483610be6565b600460008673ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020019081526020016000208190555061096a600560008673ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060003373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020019081526020016000205483610be6565b600560008673ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060003373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002081905550610a33600460008573ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002054836110b6565b600460008573ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020819055508273ffffffffffffffffffffffffffffffffffffffff168473ffffffffffffffffffffffffffffffffffffffff167fddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef846040518082815260200191505060405180910390a3600190509392505050565b600260009054906101000a900460ff1681565b60035481565b6000600460008373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020549050919050565b60008054600181600116156101000203166002900480601f016020809104026020016040519081016040528092919081815260200182805460018160011615610100020316600290048015610bde5780601f10610bb357610100808354040283529160200191610bde565b820191906000526020600020905b815481529060010190602001808311610bc157829003601f168201915b505050505081565b6000828211151515610bf757600080fd5b818303905092915050565b6000610c4d600460003373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020019081526020016000205483610be6565b600460003373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002081905550610cd9600460008573ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002054836110b6565b600460008573ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020819055508273ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff167fddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef846040518082815260200191505060405180910390a36001905092915050565b60008082111515610d9b57600080fd5b8183811515610da657fe5b04905092915050565b600082600560003373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060008673ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020819055508373ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff167f8c5be1e5ebec7d5bd14f71427d1e84f3dd0314c0f7b2291e5b200ac8c7c3b925856040518082815260200191505060405180910390a38373ffffffffffffffffffffffffffffffffffffffff16638f4ffcb1338530866040518563ffffffff167c0100000000000000000000000000000000000000000000000000000000028152600401808573ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020018481526020018373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200180602001828103825283818151815260200191508051906020019080838360005b83811015610f8c578082015181840152602081019050610f71565b50505050905090810190601f168015610fb95780820380516001836020036101000a031916815260200191505b5095505050505050600060405180830381600087803b158015610fdb57600080fd5b505af1158015610fef573d6000803e3d6000fd5b50505050600190509392505050565b60008183029050600083148061101e575081838281151561101b57fe5b04145b151561102957600080fd5b92915050565b6000600560008473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060008373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002054905092915050565b600081830190508281101515156110cc57600080fd5b929150505600a165627a7a72305820547c16fbc16bae7e15f001d85ef47fb0a162e5f62def24d96ab7bdc76ec809320029"

abi = json.loads(
    """[
    {
        "constant": true,
        "inputs": [],
        "name": "name",
        "outputs": [
            {
                "name": "",
                "type": "string"
            }
        ],
        "payable": false,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": false,
        "inputs": [
            {
                "name": "spender",
                "type": "address"
            },
            {
                "name": "tokens",
                "type": "uint256"
            }
        ],
        "name": "approve",
        "outputs": [
            {
                "name": "success",
                "type": "bool"
            }
        ],
        "payable": false,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": true,
        "inputs": [],
        "name": "totalSupply",
        "outputs": [
            {
                "name": "",
                "type": "uint256"
            }
        ],
        "payable": false,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": false,
        "inputs": [
            {
                "name": "from",
                "type": "address"
            },
            {
                "name": "to",
                "type": "address"
            },
            {
                "name": "tokens",
                "type": "uint256"
            }
        ],
        "name": "transferFrom",
        "outputs": [
            {
                "name": "success",
                "type": "bool"
            }
        ],
        "payable": false,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": true,
        "inputs": [],
        "name": "decimals",
        "outputs": [
            {
                "name": "",
                "type": "uint8"
            }
        ],
        "payable": false,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": true,
        "inputs": [],
        "name": "_totalSupply",
        "outputs": [
            {
                "name": "",
                "type": "uint256"
            }
        ],
        "payable": false,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": true,
        "inputs": [
            {
                "name": "tokenOwner",
                "type": "address"
            }
        ],
        "name": "balanceOf",
        "outputs": [
            {
                "name": "balance",
                "type": "uint256"
            }
        ],
        "payable": false,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": true,
        "inputs": [],
        "name": "symbol",
        "outputs": [
            {
                "name": "",
                "type": "string"
            }
        ],
        "payable": false,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": true,
        "inputs": [
            {
                "name": "a",
                "type": "uint256"
            },
            {
                "name": "b",
                "type": "uint256"
            }
        ],
        "name": "safeSub",
        "outputs": [
            {
                "name": "c",
                "type": "uint256"
            }
        ],
        "payable": false,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": false,
        "inputs": [
            {
                "name": "to",
                "type": "address"
            },
            {
                "name": "tokens",
                "type": "uint256"
            }
        ],
        "name": "transfer",
        "outputs": [
            {
                "name": "success",
                "type": "bool"
            }
        ],
        "payable": false,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": true,
        "inputs": [
            {
                "name": "a",
                "type": "uint256"
            },
            {
                "name": "b",
                "type": "uint256"
            }
        ],
        "name": "safeDiv",
        "outputs": [
            {
                "name": "c",
                "type": "uint256"
            }
        ],
        "payable": false,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": false,
        "inputs": [
            {
                "name": "spender",
                "type": "address"
            },
            {
                "name": "tokens",
                "type": "uint256"
            },
            {
                "name": "data",
                "type": "bytes"
            }
        ],
        "name": "approveAndCall",
        "outputs": [
            {
                "name": "success",
                "type": "bool"
            }
        ],
        "payable": false,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": true,
        "inputs": [
            {
                "name": "a",
                "type": "uint256"
            },
            {
                "name": "b",
                "type": "uint256"
            }
        ],
        "name": "safeMul",
        "outputs": [
            {
                "name": "c",
                "type": "uint256"
            }
        ],
        "payable": false,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": true,
        "inputs": [
            {
                "name": "tokenOwner",
                "type": "address"
            },
            {
                "name": "spender",
                "type": "address"
            }
        ],
        "name": "allowance",
        "outputs": [
            {
                "name": "remaining",
                "type": "uint256"
            }
        ],
        "payable": false,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": true,
        "inputs": [
            {
                "name": "a",
                "type": "uint256"
            },
            {
                "name": "b",
                "type": "uint256"
            }
        ],
        "name": "safeAdd",
        "outputs": [
            {
                "name": "c",
                "type": "uint256"
            }
        ],
        "payable": false,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "payable": false,
        "stateMutability": "nonpayable",
        "type": "constructor"
    },
    {
        "payable": true,
        "stateMutability": "payable",
        "type": "fallback"
    },
    {
        "anonymous": false,
        "inputs": [
            {
                "indexed": true,
                "name": "from",
                "type": "address"
            },
            {
                "indexed": true,
                "name": "to",
                "type": "address"
            },
            {
                "indexed": false,
                "name": "tokens",
                "type": "uint256"
            }
        ],
        "name": "Transfer",
        "type": "event"
    },
    {
        "anonymous": false,
        "inputs": [
            {
                "indexed": true,
                "name": "tokenOwner",
                "type": "address"
            },
            {
                "indexed": true,
                "name": "spender",
                "type": "address"
            },
            {
                "indexed": false,
                "name": "tokens",
                "type": "uint256"
            }
        ],
        "name": "Approval",
        "type": "event"
    }
]"""
)


class ContractAddress(rlp.Serializable):
    fields = [
        ("from", rlp.sedes.Binary()),
        ("nonce", rlp.sedes.big_endian_int),
    ]


def test_erc20_contract(w3):
    acct = eth_account.Account.from_key(KEYS["validator"])

    erc20_contract = w3.eth.contract(abi=abi, bytecode=bytecode)
    tx = erc20_contract.constructor().buildTransaction(
        {
            "gas": 3000000,
            "nonce": w3.eth.get_transaction_count(acct.address, "pending"),
        }
    )
    signed = eth_account.Account.sign_transaction(tx, KEYS["validator"])
    txhash = w3.eth.send_raw_transaction(signed.rawTransaction)
    print("deploy contract tx", txhash.hex())
    tx = waittx(w3, txhash)
    print("deploy contract receipt", tx)
    assert tx.status == 1, "tx failed"
    tx_ = w3.eth.get_transaction(txhash)
    print("deploy contract tx", tx_)

    # verify contract address
    print("create address", acct.address, tx_.nonce)
    expect_contract_addr = contract_address(acct.address, tx_.nonce)
    print(
        "contract address, expected:",
        expect_contract_addr,
        "actual:",
        tx.contractAddress,
    )
    assert expect_contract_addr == tx.contractAddress, "invalid contract address"

    print("get code back", len(w3.eth.get_code(tx.contractAddress)))

    contract = w3.eth.contract(address=tx.contractAddress, abi=abi)

    # check balance
    print(
        "balances",
        acct.address,
        contract.functions.balanceOf(acct.address).call({"from": acct.address}),
        ADDRS["community"],
        contract.functions.balanceOf(ADDRS["community"]).call({"from": acct.address}),
    )

    txhash = contract.functions.transfer(ADDRS["community"], 10).transact(
        {"from": acct.address}
    )
    print("transfer tx", txhash.hex())
    tx = waittx(w3, txhash)
    print("transfer", tx)
    assert tx.status == 1, "tx failed"

    assert len(tx.logs) > 0, "empty logs"

    # check balance
    # FIXME need to set `from` field for ethermint
    print(
        "balances",
        acct.address,
        contract.functions.balanceOf(acct.address).call({"from": acct.address}),
        ADDRS["community"],
        contract.functions.balanceOf(ADDRS["community"]).call({"from": acct.address}),
    )

    print("get block", w3.eth.get_block(tx.blockNumber))

    block = w3.eth.get_block(tx.blockNumber)
    print("transfer block", block)
    assert block.logsBloom == tx.logsBloom, "invalid block logs bloom"

    # build transaction without from field
    with pytest.raises(Exception):
        contract.functions.transfer(ADDRS["community"], 10).buildTransaction(
            {
                "nonce": w3.eth.get_transaction_count(acct.address, "pending"),
            }
        )

    # offline build transfer
    tx = contract.functions.transfer(ADDRS["community"], 10).buildTransaction(
        {
            "from": acct.address,
            "nonce": w3.eth.get_transaction_count(acct.address, "pending"),
        }
    )
    signed = eth_account.Account.sign_transaction(tx, KEYS["validator"])
    txhash = w3.eth.send_raw_transaction(signed.rawTransaction)
    txreceipt = waittx(w3, txhash)
    print("receipt", txreceipt)
    # assert len(tx.logs) > 0, "empty logs"
    assert tx["gas"] == 34466

    # check balance
    print(
        "balances",
        acct.address,
        contract.functions.balanceOf(acct.address).call({"from": acct.address}),
        ADDRS["community"],
        contract.functions.balanceOf(ADDRS["community"]).call({"from": acct.address}),
    )


def test_erc20_contract2(w3):
    """
    port the unit test in ethermint repo
    """
    bytecode = "608060405234801561001057600080fd5b506040516113913803806113918339818101604052604081101561003357600080fd5b810190808051906020019092919080519060200190929190505050806000808473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020819055508060028190555050506112e8806100a96000396000f3fe608060405234801561001057600080fd5b50600436106100935760003560e01c8063661884631161006657806366188463146101f057806370a0823114610256578063a9059cbb146102ae578063d73dd62314610314578063dd62ed3e1461037a57610093565b8063095ea7b31461009857806318160ddd146100fe57806323b872dd1461011c57806340c10f19146101a2575b600080fd5b6100e4600480360360408110156100ae57600080fd5b81019080803573ffffffffffffffffffffffffffffffffffffffff169060200190929190803590602001909291905050506103f2565b604051808215151515815260200191505060405180910390f35b6101066104e4565b6040518082815260200191505060405180910390f35b6101886004803603606081101561013257600080fd5b81019080803573ffffffffffffffffffffffffffffffffffffffff169060200190929190803573ffffffffffffffffffffffffffffffffffffffff169060200190929190803590602001909291905050506104ee565b604051808215151515815260200191505060405180910390f35b6101ee600480360360408110156101b857600080fd5b81019080803573ffffffffffffffffffffffffffffffffffffffff169060200190929190803590602001909291905050506108a3565b005b61023c6004803603604081101561020657600080fd5b81019080803573ffffffffffffffffffffffffffffffffffffffff16906020019092919080359060200190929190505050610955565b604051808215151515815260200191505060405180910390f35b6102986004803603602081101561026c57600080fd5b81019080803573ffffffffffffffffffffffffffffffffffffffff169060200190929190505050610be5565b6040518082815260200191505060405180910390f35b6102fa600480360360408110156102c457600080fd5b81019080803573ffffffffffffffffffffffffffffffffffffffff16906020019092919080359060200190929190505050610c2d565b604051808215151515815260200191505060405180910390f35b6103606004803603604081101561032a57600080fd5b81019080803573ffffffffffffffffffffffffffffffffffffffff16906020019092919080359060200190929190505050610e49565b604051808215151515815260200191505060405180910390f35b6103dc6004803603604081101561039057600080fd5b81019080803573ffffffffffffffffffffffffffffffffffffffff169060200190929190803573ffffffffffffffffffffffffffffffffffffffff169060200190929190505050611045565b6040518082815260200191505060405180910390f35b600081600160003373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060008573ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020819055508273ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff167f8c5be1e5ebec7d5bd14f71427d1e84f3dd0314c0f7b2291e5b200ac8c7c3b925846040518082815260200191505060405180910390a36001905092915050565b6000600254905090565b60008060008573ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020019081526020016000205482111561053b57600080fd5b600160008573ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060003373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020548211156105c457600080fd5b600073ffffffffffffffffffffffffffffffffffffffff168373ffffffffffffffffffffffffffffffffffffffff1614156105fe57600080fd5b61064f826000808773ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020546110cc90919063ffffffff16565b6000808673ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020819055506106e2826000808673ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020546111c090919063ffffffff16565b6000808573ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020819055506107b382600160008773ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060003373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020546110cc90919063ffffffff16565b600160008673ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060003373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020819055508273ffffffffffffffffffffffffffffffffffffffff168473ffffffffffffffffffffffffffffffffffffffff167fddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef846040518082815260200191505060405180910390a3600190509392505050565b6108f4816000808573ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020546111c090919063ffffffff16565b6000808473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020019081526020016000208190555061094b816002546111c090919063ffffffff16565b6002819055505050565b600080600160003373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060008573ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020549050808310610a65576000600160003373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060008673ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002081905550610af9565b610a7883826110cc90919063ffffffff16565b600160003373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060008673ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020819055505b8373ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff167f8c5be1e5ebec7d5bd14f71427d1e84f3dd0314c0f7b2291e5b200ac8c7c3b925600160003373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060008873ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020546040518082815260200191505060405180910390a3600191505092915050565b60008060008373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020549050919050565b60008060003373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002054821115610c7a57600080fd5b600073ffffffffffffffffffffffffffffffffffffffff168373ffffffffffffffffffffffffffffffffffffffff161415610cb457600080fd5b610d05826000803373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020546110cc90919063ffffffff16565b6000803373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002081905550610d98826000808673ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020546111c090919063ffffffff16565b6000808573ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020819055508273ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff167fddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef846040518082815260200191505060405180910390a36001905092915050565b6000610eda82600160003373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060008673ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020546111c090919063ffffffff16565b600160003373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060008573ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020819055508273ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff167f8c5be1e5ebec7d5bd14f71427d1e84f3dd0314c0f7b2291e5b200ac8c7c3b925600160003373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060008773ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020546040518082815260200191505060405180910390a36001905092915050565b6000600160008473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060008373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002054905092915050565b6000828211156040518060400160405280601281526020017f4d4154485f5355425f554e444552464c4f570000000000000000000000000000815250906111ae576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004018080602001828103825283818151815260200191508051906020019080838360005b83811015611173578082015181840152602081019050611158565b50505050905090810190601f1680156111a05780820380516001836020036101000a031916815260200191505b509250505060405180910390fd5b50600082840390508091505092915050565b6000808284019050838110156040518060400160405280601181526020017f4d4154485f4144445f4f564552464c4f57000000000000000000000000000000815250906112a8576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004018080602001828103825283818151815260200191508051906020019080838360005b8381101561126d578082015181840152602081019050611252565b50505050905090810190601f16801561129a5780820380516001836020036101000a031916815260200191505b509250505060405180910390fd5b50809150509291505056fea265627a7a72315820d78a33bfcaf696ab45393e8e57e6cd526c981fcdef7b30c0f5c93baca905bf3764736f6c63430005110032"
    abi = json.loads(
        """[{"inputs":[{"internalType":"address","name":"initialAccount","type":"address"},{"internalType":"uint256","name":"initialBalance","type":"uint256"}],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"spender","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"constant":true,"inputs":[{"internalType":"address","name":"_owner","type":"address"},{"internalType":"address","name":"_spender","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"_spender","type":"address"},{"internalType":"uint256","name":"_value","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"_owner","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"_spender","type":"address"},{"internalType":"uint256","name":"_subtractedValue","type":"uint256"}],"name":"decreaseApproval","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"_spender","type":"address"},{"internalType":"uint256","name":"_addedValue","type":"uint256"}],"name":"increaseApproval","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"account","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"mint","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"_to","type":"address"},{"internalType":"uint256","name":"_value","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"_from","type":"address"},{"internalType":"address","name":"_to","type":"address"},{"internalType":"uint256","name":"_value","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"}]"""
    )
    acct = eth_account.Account.from_key(KEYS["validator"])
    contract = w3.eth.contract(abi=abi, bytecode=bytecode)
    txhash = contract.constructor(acct.address, 1000 * (10 ** 18)).transact(
        {"from": acct.address}
    )
    tx = waittx(w3, txhash)
    assert tx["gasUsed"] == 1144643, "wrong gas used"
    print("create receipt", tx)

    # transfer
    contract = w3.eth.contract(address=tx.contractAddress, abi=abi)
    args = contract.functions.transfer(ADDRS["community"], 1000).buildTransaction(
        {
            "from": acct.address,
            "nonce": w3.eth.get_transaction_count(acct.address, "pending"),
        }
    )
    print("args", args)
    args["gas"] = w3.eth.estimate_gas(args)
    signed = eth_account.Account.sign_transaction(args, KEYS["validator"])
    txhash = w3.eth.send_raw_transaction(signed.rawTransaction)
    tx = waittx(w3, txhash)
    assert tx["gasUsed"] == args["gas"] == 51880, "wrong gas used"
    print("transfer receipt", tx)
