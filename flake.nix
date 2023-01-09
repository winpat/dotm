{
  description = "A symlink-based dotfile manager with support for multiple hosts";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-22.11";
  };

  outputs = { self, nixpkgs }:
    let pkgs = nixpkgs.legacyPackages.x86_64-linux;
        deps = [
          pkgs.python3
          pkgs.python3Packages.pyyaml
          pkgs.python3Packages.types-pyyaml
          pkgs.python3Packages.pytest
          pkgs.python3Packages.pytest-mock
          pkgs.python3Packages.pytest-isort
          pkgs.python3Packages.pytest-flake8
          pkgs.python3Packages.pytest-black
          pkgs.python3Packages.pytest-mypy
          pkgs.python3Packages.ipdb
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
