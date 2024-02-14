import re
from collections import defaultdict, deque
from pathlib import Path
from typing import Dict, NamedTuple

from dotm.dotfile import Dotfile


def load_config(source_directory: Path) -> Dict:
    """Load .dotrc file from source directory."""
    config_file = source_directory / ".dotrc"

    if not config_file.is_file():
        print("Source directory does not contain a .dotrc file")
        exit(1)

    try:
        return parse_config(config_file.read_text())
    except:
        print(".dotrc is invalid")
        exit(1)


def parse_config(text: str):
    """Parse the dotrc configuration file."""
    cwd = Path.cwd()
    home = Path.home()

    cfg = defaultdict(list)
    line_nr = 0
    hosts = []

    for line_nr, line in enumerate(text.split("\n")):
        match line.split():
            case []:
                continue
            case [host_group] if host_group.endswith(":"):
                hosts = host_group.removesuffix(":").split("|")
            case ["-", name]:
                df = Dotfile(path=name, source=cwd / name, target=home / name)
                for host in hosts:
                    cfg[host].append(df)
            case ["-", name, "->", target]:
                df = Dotfile(path=name, source=cwd / name, target=Path(target))
                for host in hosts:
                    cfg[host].append(df)
            case _:
                raise ValueError(f"Unable to parse parse line {line_nr}.")

    return cfg
