"""A basic dotfile manager with support for host specific configurations."""

from collections import namedtuple
from itertools import filterfalse, tee
from os import getcwd, path
from pathlib import Path
from socket import gethostname
from sys import exit

import yaml

Dotfile = namedtuple("Dotfile", ["source", "destination", "relative"])


def source_dir():
    """Return path to source directory."""
    return getcwd()


def destination_dir():
    """Return path to destination directory."""
    return path.expanduser("~")


def load_config(source_dir):
    """Load .dotrc file."""
    dotrc_path = path.join(source_dir, ".dotrc")
    if not path.isfile(dotrc_path):
        print("Source directory does not contain a .dotrc file")
        exit(1)

    with open(dotrc_path) as f:
        try:
            return yaml.load(f, Loader=yaml.BaseLoader)
        except yaml.YAMLError:
            print(".dotrc is not valid")
            exit(1)


def print_status(existing, created):
    print("The following files were not touched:")
    for df in existing:
        print(df.relative)
    print("The following were symlinked:")
    for df in created:
        print(df.relative)


def partition(pred, iterable):
    """Partition an iterable by a predicate."""
    t1, t2 = tee(iterable)
    return list(filterfalse(pred, t1)), list(filter(pred, t2))


def exists(df):
    """Check if a dotfile exists and points to the correct file."""
    # TODO: What should we do if the file is a link pointing to a different location?
    dest_path = Path(df.destination)

    if not dest_path.exists():
        return False

    if dest_path.is_symlink() and str(dest_path.resolve()) == df.source:
        return True

    print(
        f"File {df.destination} already exists and is not managed by dotm.",
        " Please remove it manually.",
    )
    exit(1)


def link(config, source_dir, dest_dir):
    """Link relevant dotfiles according to .dotrc configuration."""
    # Extract relevant links from config
    hostname = gethostname()
    file_paths = config.get(hostname, []) + config.get("all", [])

    if not file_paths:
        print(f'There are no files matching the host "{hostname}".')
        exit(1)

    dotfiles = []
    for fp in file_paths:
        source = path.join(source_dir, fp)
        if not path.isfile(source):
            print(f"Source file {source} does not exist!")
            exit(1)

        dest = path.join(dest_dir, fp)
        dotfiles.append(Dotfile(source, dest, fp))

    missing, existing = partition(exists, dotfiles)
    for p in missing:
        Path(p.destination).symlink_to(p.source)

    print_status(existing, missing)
    return existing, missing


def main():
    source = source_dir()
    dest = destination_dir()
    config = load_config(source)
    link(config, source, dest)


if __name__ == "__main__":
    main()
