import pytest

from dotm.conftest import touch_dotrc
from dotm.dotfile import Dotfile


@pytest.fixture
def dotfile(source_dir, target_dir) -> Dotfile:
    dotfile = ".emacs"
    return Dotfile(dotfile, source_dir / dotfile, target_dir / dotfile)


def test_exists(dotfile):
    assert not dotfile.exists
    dotfile.source.touch()
    assert dotfile.exists


def test_conflicts(source_dir, dotfile):
    config = {"all": [dotfile.path]}
    touch_dotrc(source_dir, config)

    dotfile.link()
    assert not dotfile.conflicts

    other_file = source_dir / "otherfile"
    other_file.touch()

    dotfile.target.unlink()
    dotfile.target.symlink_to(other_file)
    assert dotfile.conflicts


def test_linked(source_dir, dotfile):
    config = {"all": [dotfile.path]}
    touch_dotrc(source_dir, config)

    assert not dotfile.linked
    dotfile.link()
    assert dotfile.linked


def test_link(dotfile):
    dotfile.source.touch()

    correctly_created = lambda df: df.exists and df.linked and not df.conflicts

    assert not correctly_created(dotfile)
    dotfile.link()
    assert correctly_created(dotfile)
