from pathlib import Path
from typing import NamedTuple


class Dotfile(NamedTuple):
    path: str
    source: Path
    target: Path

    def __str__(self) -> str:
        return self.path

    @property
    def exists(self) -> bool:
        """Check if source of dotfile is a file or directory."""
        return self.source.is_file() or self.source.is_dir()

    @property
    def linked(self) -> bool:
        """Check if target of dotfile is a symbolic link."""
        return self.target.resolve() == self.source

    @property
    def conflicts(self) -> bool:
        """Check if target exist and points to a file other than the source."""
        return self.target.resolve() != self.source

    def link(self) -> None:
        """Symlink target to source."""
        self.target.symlink_to(self.source)
