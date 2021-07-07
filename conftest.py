import subprocess
from pathlib import Path

import pytest
import web3


def setup_ethermint(path):
    config_path = Path(__file__).parent / "config.yaml"
    proc = subprocess.Popen(
        ["pystarport", "serve", "--config", config_path, "--data", path]
    )
    try:
        # wait for block 1
        yield web3.Web3(web3.providers.HTTPProvider("http://localhost:1317"))
    finally:
        proc.terminate()
        proc.wait()


def setup_geth(path):
    proc = subprocess.Popen(
        [
            "geth",
            "--datadir",
            path,
            "--http",
            "--dev",
            "--dev.period",
            "2",
            "--http.corsdomain" '"*"',
        ]
    )
    try:
        # wait for block 1
        yield web3.Web3(web3.providers.HTTPProvider("http://localhost:8485"))
    finally:
        proc.terminate()
        proc.wait()


@pytest.fixture(scope="session", params={"type": ["ethermint", "geth"]})
def w3(tmp_path, type):
    path = tmp_path / "ethermint"
    if type == "ethermint":
        yield from setup_ethermint(path)
    elif type == "geth":
        yield from setup_geth(path)
    else:
        raise NotImplementedError
