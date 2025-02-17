from pathlib import Path

import pytest

from dotm.config import load_config, parse_config
from dotm.dotfile import Dotfile


def test_missing_dotrc(source_dir, target_dir, capsys):
    with pytest.raises(SystemExit) as excinfo:
        load_config(source_dir, target_dir)

    stderr = capsys.readouterr().out
    assert stderr == "Source directory does not contain a .dotrc file\n"
    assert excinfo.value.code == 1


def test_invalid_dotrc(source_dir, target_dir, capsys):
    dotrc = Path(source_dir) / ".dotrc"
    dotrc.write_text("key: value: other")

    with pytest.raises(SystemExit) as excinfo:
        load_config(source_dir, target_dir)

    stderr = capsys.readouterr().out
    assert stderr == "Unable to parse parse line 0: key: value: other\n"
    assert excinfo.value.code == 1


def test_parse_config(source_dir, target_dir):
    cfg = """
all:
 - .bashrc

tron:
 - .emacs
    """

    assert parse_config(cfg, source_dir, target_dir) == {
        "all": [
            Dotfile(
                name=".bashrc",
                source=source_dir / ".bashrc",
                target=target_dir / ".bashrc",
            )
        ],
        "tron": [
            Dotfile(
                name=".emacs",
                source=source_dir / ".emacs",
                target=target_dir / ".emacs",
            )
        ],
    }
