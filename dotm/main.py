"""A basic dotfile manager with support for host specific configurations."""

from pathlib import Path
from socket import gethostname
from sys import exit
from typing import Dict, List, Tuple

from dotm.config import load_config
from dotm.dotfile import Dotfile, conflicts, exists, link, linked


def get_relevant_files(config: Dict) -> List[str]:
    """Collect relevant files for host."""
    hostname = gethostname()
    relevant: List[str] = []

    for host_set, files in config.items():
        if hostname in host_set.split("|") or host_set == "all":
            relevant.extend(files)

    return relevant


def path_to_dotfile(
    path: str, source_directory: Path, target_directory: Path
) -> Dotfile:
    """Create a dotfile object from a path string.

    If the path string contains "->" with a subsequent filesystem path, the
    target location will be overriden with that path:
    """

    # Check if path contains target override.
    if " -> " in path:
        path, override = path.split(" -> ", 1)
        return Dotfile(path, source_directory / path, Path(override))

    return Dotfile(path, source_directory / path, target_directory / path)


def dotm(config: Dict, source_directory: Path, target_directory: Path) -> Tuple:
    """Link relevant dotfiles according to .dotrc configuration."""

    relevant_files = get_relevant_files(config)
    if not relevant_files:
        print("There are no files matching the host.")
        exit(1)

    existing = []
    new = []
    for path in relevant_files:

        df = path_to_dotfile(path, source_directory, target_directory)

        if not exists(df):
            print(f"Source {df.source} of dotfile {df.path} does not exist!")
            exit(1)

        if linked(df):
            if conflicts(df):
                print(
                    f"Target file {df.target} already exists."
                    " Please resolve the conflict manually!"
                )
                exit(1)
            else:
                existing.append(df)
                continue

        new.append(df)

    for df in new:
        link(df)
        print(df.path)

    return existing, new


def main():
    dotm(
        config=load_config(Path.cwd()),
        source_directory=Path.cwd(),
        target_directory=Path.home(),
    )


if __name__ == "__main__":
    main()
