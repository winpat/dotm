from pathlib import Path
from typing import NamedTuple


class Dotfile(NamedTuple):
    path: str
    source: Path
    target: Path

    def __str__(self) -> str:
        return self.path


def exists(df: Dotfile) -> bool:
    """Check if the source of a dotfile is a file or directory."""
    return df.source.is_file() or df.source.is_dir()


def linked(df: Dotfile) -> bool:
    """Check if the target of a dotfile is a symbolic link."""
    return df.target.resolve() == df.source


def conflicts(df: Dotfile) -> bool:
    """Check if the target points to a file other than the source file."""
    return df.target.resolve() != df.source


def link(df: Dotfile) -> None:
    """Symlink target of dotfile to source."""
    df.target.symlink_to(df.source)
