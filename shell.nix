{ pkgs ? import ./nix {} }:
let b = import ./. { inherit pkgs; };
in pkgs.mkShell {
  buildInputs = [
    b.test-pyenv
    pkgs.go-ethereum
    pkgs.ethermint
  ];
}
