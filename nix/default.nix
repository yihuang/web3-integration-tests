{ sources ? import ./sources.nix, system ? builtins.currentSystem }:

import sources.nixpkgs {
  overlays = [
    (_: pkgs: {
      ethermint = pkgs.buildGoModule rec {
        name = "ethermint";
        src = sources.ethermint;
        subPackages = [ "./cmd/ethermintd" ];
        vendorSha256 = sha256:0l60mysv18x05k2qh9gvhzsy35s2kv1x8jvbb1vc6x1calmp9nk4;
        doCheck = false;
      };
    })
  ];
  config = { };
  inherit system;
}
