{ system ? builtins.currentSystem, pkgs ? import ./nix { inherit system; } }:
{
  inherit pkgs;
  # python env for python linter tools and pytest
  test-pyenv = pkgs.poetry2nix.mkPoetryEnv { projectDir = ./.; };
  scripts = (pkgs.callPackage ./nix/scripts.nix
    {
      config = {
        ethermint-config = ./scripts/ethermint-config.yaml;
        geth-genesis = ./scripts/geth-genesis.json;
      };
    }).scripts-env;
}

