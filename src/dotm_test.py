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


def test_invalid_dotrc(source_dir, capsys):
    dotrc = Path(source_dir) / ".dotrc"
    dotrc.write_text("somekey: somevalue: someothervalue")

    with pytest.raises(SystemExit) as we:
        load_config(source_dir)
        assert we.value.code == 1

    captured = capsys.readouterr()
    assert captured.out == ".dotrc is not valid\n"


def test_host_specific_dotrc(source_dir, dest_dir, dotrc, mocker):

    files = touch_dotrc(source_dir, dotrc)
    mocker.patch("dotm.gethostname", return_value="host1")

    link(dotrc, source_dir, dest_dir)

    for f in files:
        p = Path(f"{dest_dir}/{f}")
        assert p.is_symlink()
        assert p.resolve(f"{source_dir}/{f}")


def test_existing_dotfile(source_dir, dest_dir):
    dotfile = ".emacs"
    dotrc = {"all": [dotfile]}
    touch_dotrc(source_dir, dotrc)

    # Ensure the link exists
    source_file = Path(source_dir, dotfile)
    link_target = Path(dest_dir, dotfile)
    link_target.symlink_to(source_file)

    existing, missing = link(dotrc, source_dir, dest_dir)
    assert len(existing) == 1
    assert len(missing) == 0


def test_missing_dotfile(source_dir, dest_dir):
    dotfile = ".emacs"
    dotrc = {"all": [dotfile]}
    touch_dotrc(source_dir, dotrc)

    existing, missing = link(dotrc, source_dir, dest_dir)
    assert len(missing) == 1
    assert len(existing) == 0
