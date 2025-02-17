"""A basic dotfile manager with support for host specific configurations."""

from pathlib import Path
from socket import gethostname
from sys import exit

from dotm.config import load_config
from dotm.dotfile import Dotfile


def get_relevant_files(config: dict) -> list[Dotfile]:
    """Collect relevant files for host."""
    hostname = gethostname()

    relevant = []
    for host, files in config.items():
        if host == hostname or host == "all":
            relevant.extend(files)

    if not relevant:
        raise ValueError(f'No files matching host "{hostname}".')

    return relevant


def dotm(
    config: dict, source_dir: Path, target_dir: Path
) -> tuple[list[Dotfile], list[Dotfile]]:
    """Link relevant dotfiles according to .dotrc configuration."""

    try:
        relevant_files = get_relevant_files(config)
    except ValueError as exc:
        print(exc)
        exit(1)

    existing = []
    new = []
    for df in relevant_files:
        if not df.exists:
            print(f"Source {df.source} of dotfile {df.name} does not exist!")
            exit(1)

        if df.linked:
            if df.conflicts:
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
        df.link
        print(df.name)

    return existing, new


def main():
    working_dir = Path.cwd()
    home_dir = Path.home()

    dotm(
        config=load_config(working_dir, home_dir),
        source_dir=working_dir,
        target_dir=home_dir,
    )


if __name__ == "__main__":
    main()
