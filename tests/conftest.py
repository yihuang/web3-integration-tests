import os
import signal
import socket
import subprocess
import time

import pytest
import web3
from web3.middleware import geth_poa_middleware


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
    proc = subprocess.Popen(["start-ethermint", path], preexec_fn=os.setsid)
    try:
        wait_for_port(1317)
        yield web3.Web3(web3.providers.HTTPProvider("http://localhost:1317"))
    finally:
        os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
        # proc.terminate()
        proc.wait()


def setup_geth(path):
    proc = subprocess.Popen(["start-geth", path], preexec_fn=os.setsid)
    try:
        ipc_path = path / "geth.ipc"
        wait_for_ipc(ipc_path)
        w3 = web3.Web3(web3.providers.IPCProvider(ipc_path))
        w3.middleware_onion.inject(geth_poa_middleware, layer=0)
        time.sleep(1)
        yield w3
    finally:
        os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
        # proc.terminate()
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
