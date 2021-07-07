Integration tests run against both geth and ethermint. Geth runs in dev mode, ethermint devnet is start by pystarport.

## Run the tests

```shell
$ nix-shell
<nix-shell> $ pytest
```

```shell
<nix-shell> $ # run against ethermint only
<nix-shell> $ pytest -k ethermint
<nix-shell> $ # run against geth only
<nix-shell> $ pytest -k geth
```

