with import <nixpkgs> {};


stdenv.mkDerivation {
  name = "env";
  buildInputs = [
    python3
    python3Packages.pyyaml

    # Developement
    python3Packages.pytest
    python3Packages.pytest-mock
    python3Packages.pytest-isort
    python3Packages.pytest-flake8
    python3Packages.pytest-black
    python3Packages.pytest-mypy
    python3Packages.ipdb
  ];
}
