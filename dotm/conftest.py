from pathlib import Path

import pytest
import yaml


@pytest.fixture
def source_dir(tmp_path):
    source = tmp_path / "source"
    source.mkdir()
    return str(source)


@pytest.fixture
def dest_dir(tmp_path):
    dest = tmp_path / "destination"
    dest.mkdir()
    return str(dest)


@pytest.fixture
def dotrc(source_dir, dest_dir):
    return {"all": [".emacs", ".tmux.conf"], "host1": [".vimrc"]}


def touch_dotrc(source_dir, dotrc):
    files = flatten(dotrc.values())
    for f in files:
        Path(f"{source_dir}/{f}").touch()
    with open(f"{source_dir}/.dotrc", "w") as f:
        yaml.dump(dotrc, f)
    return files


def flatten(l):
    return [i for sl in l for i in sl]
