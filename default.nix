with import <nixpkgs> {};

python3.pkgs.buildPythonApplication rec {
  name = "dotm";
  src = ./.;
  propagatedBuildInputs = [
    python37
    python37Packages.pyyaml
    python37Packages.pytest
  ];
}
