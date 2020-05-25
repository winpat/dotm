from pathlib import Path

import pytest

from conftest import touch_dotrc
from dotm import link, load_config


def test_missing_dotrc(source_dir, capsys):
    with pytest.raises(SystemExit) as we:
        load_config(source_dir)
        assert we.value.code == 1

    captured = capsys.readouterr()
    assert captured.out == "Source directory does not contain a .dotrc file\n"


def test_link(source_dir, dest_dir, dotrc, mocker):

    files = touch_dotrc(source_dir, dotrc)
    mocker.patch("dotm.gethostname", return_value="host1")

    link(dotrc, source_dir, dest_dir)

    for f in files:
        p = Path(f"{dest_dir}/{f}")
        assert p.is_symlink()
        assert p.resolve(f"{source_dir}/{f}")


def test_invalid_dotrc(source_dir, capsys):
    dotrc = Path(source_dir) / ".dotrc"
    dotrc.write_text("somekey: somevalue: someothervalue")

    with pytest.raises(SystemExit) as we:
        load_config(source_dir)
        assert we.value.code == 1

    captured = capsys.readouterr()
    assert captured.out == ".dotrc is not valid\n"
