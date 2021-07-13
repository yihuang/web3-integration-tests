{ sources ? import ./sources.nix, system ? builtins.currentSystem }:

import sources.nixpkgs {
  overlays = [
    (_: pkgs: {
      ethermint = pkgs.buildGoModule rec {
        name = "ethermint";
        src = sources.ethermint;
        subPackages = [ "./cmd/ethermintd" ];
        vendorSha256 = sha256:1pk3xdwa4bb4wqzzqb7zw2m915ycmwjijnrr43y4f1jjyjjlv058;
        doCheck = false;
      };
    })
  ];
  config = { };
  inherit system;
}
