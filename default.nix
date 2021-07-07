{ system ? builtins.currentSystem, pkgs ? import ./nix { inherit system; } }:
{
  inherit (pkgs) ethermint;
  # python env for python linter tools and pytest
  test-pyenv = pkgs.poetry2nix.mkPoetryEnv { projectDir = ./.; };
}

