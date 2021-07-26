{ sources ? import ./sources.nix, system ? builtins.currentSystem }:

import sources.nixpkgs {
  overlays = [
    (_: pkgs: {
      ethermint = pkgs.buildGoModule rec {
        name = "ethermint";
        src = sources.ethermint;
        subPackages = [ "./cmd/ethermintd" ];
        vendorSha256 = sha256:05mwdh2h3svajxzj1n69zlhbb5zvlln8hp14ij30fyxgv34p2qk1;
        doCheck = false;
      };
      pystarport = pkgs.poetry2nix.mkPoetryApplication {
        projectDir = sources.pystarport;
        src = sources.pystarport;
      };
    })
  ];
  config = { };
  inherit system;
}
