# dotm

[![Build](https://github.com/winpat/dotm/workflows/Test/badge.svg)](https://github.com/winpat/dotm/actions?query=workflow%3ATest+branch%3Amaster)

A dotfile manager with support for host specific configuration.

## Installation

Use the [nix package manager](https://nixos.org/nix) to install dotm.

```bash
nix profile install github:winpat/dotm
```

## Usage

Add a .dotrc file to your dotfiles repository. The dotrc file describes which
files should be linked depending on the hostname. If you want to link a file
on every host, configure it under the "all" key:

```
all:
  - .emacs
  - .tmux.conf
  - .bashrc
laptop|desktop:
  - .config/dunst
laptop:
  - .config/i3
  - nixos/laptop.nix -> /etc/nixos/configuration.nix
desktop:
  - .config/openbox
  - nixos/desktop.nix -> /etc/nixos/configuration.nix
```

Then simply run dotm in the same directory:
```bash
dotm
```

## Development

You can spawn an environment with all dependencies using nix-shell:

```bash
nix develop
```

To run the suite, simply launch pytest through the make target:

```bash
nix develop --check
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[GPLv3](https://choosealicense.com/licenses/gpl-3.0/)
