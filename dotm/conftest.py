from pathlib import Path
from typing import Any, Dict, Iterable, List

import pytest
import yaml

from dotm.dotfile import Dotfile


@pytest.fixture
def source_directory(tmp_path) -> Path:
    source = tmp_path / "source"
    source.mkdir()
    return source


@pytest.fixture
def target_directory(tmp_path) -> Path:
    target = tmp_path / "destination"
    target.mkdir()
    return target


@pytest.fixture
def dotfile(source_directory, target_directory):
    dotfile = ".emacs"
    return Dotfile(dotfile, source_directory / dotfile, target_directory / dotfile)


@pytest.fixture
def dotrc(source_directory, target_directory) -> Dict[str, List[str]]:
    return {"all": [".emacs", ".tmux.conf"], "host1": [".vimrc"]}


def touch_dotrc(source_directory: Path, dotrc: Dict[str, List[str]]) -> List:
    files = flatten(dotrc.values())
    with open(f"{source_directory}/.dotrc", "w") as f:
        yaml.dump(dotrc, f)
    for f in files:
        (source_directory / str(f)).touch()
    return files


def flatten(iterable: Iterable[Iterable[Any]]) -> List:
    return [element for sublist in iterable for element in sublist]
