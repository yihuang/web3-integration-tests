import os
import socket
import subprocess
import tempfile
import time
from pathlib import Path

import pytest
import web3
from web3.middleware import geth_poa_middleware

from .utils import ADDRS, KEYS


def wait_for_port(port, host="127.0.0.1", timeout=40.0):
    print("wait for port", port, "to be available")
    start_time = time.perf_counter()
    while True:
        try:
            with socket.create_connection((host, port), timeout=timeout):
                break
        except OSError as ex:
            time.sleep(0.1)
            if time.perf_counter() - start_time >= timeout:
                raise TimeoutError(
                    "Waited too long for the port {} on host {} to start accepting "
                    "connections.".format(port, host)
                ) from ex


def wait_for_ipc(path, timeout=40.0):
    print("wait for unix socket", path, "to be available")
    start_time = time.perf_counter()
    while True:
        if os.path.exists(path):
            break
        time.sleep(0.1)
        if time.perf_counter() - start_time >= timeout:
            raise TimeoutError(
                "Waited too long for the unix socket {path} to be available"
            )


def setup_ethermint(path):
    config_path = Path(__file__).parent / "config.yaml"
    proc = subprocess.Popen(
        ["pystarport", "serve", "--config", config_path, "--data", path]
    )
    try:
        wait_for_port(1317)
        yield web3.Web3(web3.providers.HTTPProvider("http://localhost:1317"))
    finally:
        proc.terminate()
        proc.wait()


def geth_import_account(path, key, password):
    "import geth account"
    with tempfile.NamedTemporaryFile(mode="w+") as fp:
        fp.write(key)
        fp.flush()
        subprocess.Popen(
            f"geth --datadir {path} account import {fp.name}".split(),
            stdin=subprocess.PIPE,
        ).communicate(input=f"{password}\n{password}\n".encode())


def setup_geth(path):
    genesis = Path(__file__).parent / "geth-genesis.json"
    password = "123456"

    # init genesis
    subprocess.run(f"geth --datadir {path} init {genesis}".split(), check=True)

    # import accounts
    for key in KEYS.values():
        geth_import_account(path, key, password)

    # start
    (path / "password.txt").write_text(password)
    proc = subprocess.Popen(
        [
            "geth",
            "--datadir",
            path,
            "--http",
            "--http.addr",
            "localhost",
            "--http.api",
            "personal,eth,net,web3,txpool,miner",
            "-unlock",
            ADDRS["validator"],
            "--password",
            path / "password.txt",
            "--mine",
            "--allow-insecure-unlock",
        ]
    )

    try:
        ipc_path = path / "geth.ipc"
        wait_for_ipc(ipc_path)
        w3 = web3.Web3(web3.providers.IPCProvider(ipc_path))
        w3.middleware_onion.inject(geth_poa_middleware, layer=0)
        time.sleep(1)
        yield w3
    finally:
        proc.terminate()
        proc.wait()


@pytest.fixture(scope="session", params=["ethermint", "geth"])
def w3(request, tmp_path_factory):
    provider = request.param
    path = tmp_path_factory.mktemp(provider)
    if provider == "ethermint":
        yield from setup_ethermint(path)
    elif provider == "geth":
        yield from setup_geth(path)
    else:
        raise NotImplementedError
