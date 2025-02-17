{
  description = "A symlink-based dotfile manager with support for multiple hosts";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-24.11";
  };

  outputs = { self, nixpkgs }:
    let pkgs = nixpkgs.legacyPackages.x86_64-linux;
        deps = with pkgs; [
          python3
          python3Packages.pytest
          python3Packages.pytest-mock
          python3Packages.pytest-isort
          python3Packages.pytest-black
          python3Packages.pytest-mypy
          python3Packages.ipdb
          pyright
        ];
    in {
      devShell.x86_64-linux = pkgs.mkShell {
        buildInputs = deps;
      };
      packages.x86_64-linux.dotm = pkgs.python3Packages.buildPythonPackage rec {
          name = "dotm";
          src = ./.;
          propagatedBuildInputs = deps;
        };
      packages.x86_64-linux.default = self.packages.x86_64-linux.dotm;

    };
}
