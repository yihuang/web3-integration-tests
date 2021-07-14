with import ./. { };
pkgs.mkShell {
  buildInputs = [
    test-pyenv
    scripts
  ];
}
