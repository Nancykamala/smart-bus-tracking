{
  description = "My Nix environment configuration";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
  };

  outputs = { self, nixpkgs }: {
    defaultPackage.x86_64-linux = nixpkgs.mkShell {
      buildInputs = [
        nixpkgs.python38
        nixpkgs.sqlite
        nixpkgs.psmisc
      ];
    };
  };
}
