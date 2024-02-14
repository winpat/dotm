from pathlib import Path

import pytest

from dotm.config import load_config, parse_config
from dotm.dotfile import Dotfile


def test_missing_dotrc(source_directory, capsys):
    with pytest.raises(SystemExit) as we:
        load_config(source_directory)

    assert we.value.code == 1

    captured = capsys.readouterr()
    assert captured.out == "Source directory does not contain a .dotrc file\n"


def test_invalid_dotrc(source_directory, capsys):
    dotrc = Path(source_directory) / ".dotrc"
    dotrc.write_text("somekey: somevalue: someothervalue")

    with pytest.raises(SystemExit) as we:
        load_config(source_directory)

    assert we.value.code == 1

    captured = capsys.readouterr()
    assert captured.out == ".dotrc is invalid\n"


def test_parse_config():
    cfg = """
all:
 - .bashrc

tron:
 - .emacs
    """

    assert parse_config(cfg) == {
        "all": [
            Dotfile(
                path=".bashrc",
                source=Path.cwd() / ".bashrc",
                target=Path.home() / ".bashrc",
            )
        ],
        "tron": [
            Dotfile(
                path=".emacs",
                source=Path.cwd() / ".emacs",
                target=Path.home() / ".emacs",
            )
        ],
    }
