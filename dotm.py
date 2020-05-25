"""A basic dotfile manager with support for host specific configurations."""

import yaml

from pathlib import Path
from itertools import filterfalse, tee
from collections import namedtuple
from socket import gethostname
from os import getcwd, path, getenv
from sys import exit


Dotfile = namedtuple("Dotfile", ["source", "destination", "relative"])


def source_dir():
    src_dir = getenv("DOTM_SOURCE_DIR")
    if src_dir:
        return dir_dir
    return getcwd()


def destination_dir():
    destination = getenv("DOTM_DEST_DIR")
    if destination:
        return destination
    # Fallback to home directory
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
    return filterfalse(pred, t1), filter(pred, t2)


def exists(df):
    """Check if a dotfile exists and points to the correct file."""
    return path.realpath(df.destination) == df.source


def link(config, source_dir, dest_dir):
    # Extract relevant links from config
    hostname = gethostname()
    file_paths = [*config.get(hostname, []), *config.get("all", [])]

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


if __name__ == "__main__":
    source = source_dir()
    dest = destination_dir()
    config = load_config(source)
    link(source, dest, config)
