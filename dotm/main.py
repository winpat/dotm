"""A basic dotfile manager with support for host specific configurations."""

from collections import namedtuple
from pathlib import Path
from socket import gethostname
from sys import exit

import yaml

Dotfile = namedtuple("Dotfile", ["source", "target", "name"])


def load_config(source_dir):
    """Load .dotrc file."""
    config_file = source_dir / ".dotrc"
    if not config_file.is_file():
        print("Source directory does not contain a .dotrc file")
        exit(1)

    with config_file.open() as f:
        try:
            return yaml.load(f, Loader=yaml.BaseLoader)
        except yaml.YAMLError:
            print(".dotrc is not valid")
            exit(1)


def to_dotfile(path, source_dir, target_dir):
    """Convert a path to a dotfile.

    A path is relative to a dotfile file which gets linked from the current
    working directory to the users home directory.

    An optional target file override can be specified by appending " ->
    /absolute/path" to a path.
    """
    source = Path(source_dir, path)
    target = Path(target_dir, path)

    # Check if the path has a target override
    if " -> " in path:
        path, override = path.split(" -> ", 1)
        source = Path(source_dir, path)
        target = Path(override)

    return Dotfile(source, target, path)


def relevant_files(config):
    hostname = gethostname()
    relevant = []

    for host_set, files in config.items():
        if hostname in host_set.split("|") or host_set == "all":
            relevant.extend(files)

    if not relevant:
        print(f'There are no files matching the host "{hostname}".')
        exit(1)

    return relevant


def target_exists(dotfile):
    """Check if a dotfile exists and points to the correct file."""
    is_link = dotfile.target.is_symlink()
    points_correctly = dotfile.target.resolve() == dotfile.source
    return is_link and points_correctly


def source_exists(dotfile):
    return dotfile.source.is_file() or dotfile.source.is_dir()


def create(dotfile):
    dotfile.target.symlink_to(dotfile.source)


def conflicts(dotfile):
    exists = dotfile.target.exists()
    linked_correctly = (
        dotfile.target.is_symlink() and dotfile.target.resolve() == dotfile.source
    )
    return exists and not linked_correctly


def print_status(existing, created):
    if existing:
        print("The following files were not touched:")
        for dotfile in existing:
            print("\t", dotfile.name)
    if created:
        print("The following were symlinked:")
        for dotfile in created:
            print("\t", dotfile.name)


def link(config, source_dir, target_dir):
    """Link relevant dotfiles according to .dotrc configuration."""
    existing = []
    created = []
    for path in relevant_files(config):
        dotfile = to_dotfile(path, source_dir, target_dir)

        if not source_exists(dotfile):
            print(f"Source file {dotfile.source} does not exist!")
            exit(1)

        if conflicts(dotfile):
            print(
                f"Target file {dotfile.source} is conflicting."
                " Please resolve the conflict manually!"
            )
            exit(1)

        if target_exists(dotfile):
            existing.append(dotfile)
            continue

        create(dotfile)
        created.append(dotfile)

    print_status(existing, created)
    return existing, created


def main():
    source_dir = Path.cwd()
    target_dir = Path.home()
    config = load_config(source_dir)
    link(config, source_dir, target_dir)


if __name__ == "__main__":
    main()
