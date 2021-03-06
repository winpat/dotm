with import <nixpkgs> {};


stdenv.mkDerivation {
  name = "env";
  buildInputs = [
    python37
    python37Packages.pyyaml

    # Developement
    python37Packages.pytest
    python37Packages.pytest-mock
    python37Packages.pytest-isort
    python37Packages.pytest-flake8
    python37Packages.pytest-black
    python37Packages.pytest-mypy

    python37Packages.ipython
    python37Packages.ipdb

    python37Packages.black
    python37Packages.isort
    python37Packages.mypy

    python37Packages.python-language-server
    python37Packages.pyls-black
    python37Packages.pyls-isort
    python37Packages.pyls-mypy
  ];
}
