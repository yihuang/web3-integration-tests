{ sources ? import ./sources.nix, system ? builtins.currentSystem }:

import sources.nixpkgs {
  overlays = [
    (_: pkgs: {
      ethermint = pkgs.buildGoModule rec {
        name = "ethermint";
        src = sources.ethermint;
        subPackages = [ "./cmd/ethermintd" ];
        vendorSha256 = sha256:015fn37ffkcvn2vmdr6xqwmk0grjhvcgnbv900cpmy7ywrqjc0nw;
        doCheck = false;
      };
    })
  ];
  config = { };
  inherit system;
}
