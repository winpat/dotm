"""A basic dotfile manager with support for host specific configurations."""

from pathlib import Path
from socket import gethostname
from sys import exit
from typing import Dict, List, Tuple

from dotm.config import load_config
from dotm.dotfile import Dotfile, conflicts, exists, link, linked


def get_relevant_files(config: Dict) -> List[Dotfile]:
    """Collect relevant files for host."""
    hostname = gethostname()

    relevant = []
    for host, files in config.items():
        if host == hostname or host == "all":
            relevant.extend(files)

    if not relevant:
        raise ValueError(f'No files matching host "{hostname}".')

    return relevant


def dotm(config: Dict, source_directory: Path, target_directory: Path) -> Tuple:
    """Link relevant dotfiles according to .dotrc configuration."""

    try:
        relevant_files = get_relevant_files(config)
    except ValueError as exc:
        print(exc)
        exit(1)

    existing = []
    new = []
    for df in relevant_files:
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
    working_dir = Path.cwd()
    home_dir = Path.home()

    dotm(
        config=load_config(working_dir, home_dir),
        source_directory=working_dir,
        target_directory=home_dir,
    )


if __name__ == "__main__":
    main()
