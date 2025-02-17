from collections import defaultdict
from pathlib import Path

from dotm.dotfile import Dotfile


def load_config(source_dir: Path, target_dir: Path) -> dict:
    """Load .dotrc file from source directory."""

    config_file = source_dir / ".dotrc"

    if not config_file.is_file():
        print("Source directory does not contain a .dotrc file")
        exit(1)

    try:
        config_txt = config_file.read_text()
        return parse_config(config_txt, source_dir, target_dir)
    except ValueError as exc:
        print(exc)
        exit(1)


def parse_config(
    text: str, source_dir: Path, target_dir: Path
) -> dict[str, list[Dotfile]]:
    """Parse the .dotrc and resolve paths."""

    cfg = defaultdict(list)
    lines = text.split("\n")

    for line_nr, line in enumerate(lines):
        match line.split():
            case [host_group] if host_group.endswith(":"):
                hosts = host_group.removesuffix(":").split("|")
            case ["-", fname]:
                df = Dotfile(
                    path=fname, source=source_dir / fname, target=target_dir / fname
                )
                for host in hosts:
                    cfg[host].append(df)
            case ["-", fname, "->", target]:
                df = Dotfile(path=fname, source=source_dir / fname, target=Path(target))
                for host in hosts:
                    cfg[host].append(df)
            case []:
                continue
            case _:
                raise ValueError(f"Unable to parse parse line {line_nr}: {line}")

    return cfg
