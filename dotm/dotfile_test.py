from dotm.conftest import touch_dotrc
from dotm.dotfile import Dotfile, conflicts, exists, link, linked


def test_exists(dotfile):
    assert not exists(dotfile)
    dotfile.source.touch()
    assert exists(dotfile)


def test_conflicts(source_dir, target_dir, dotfile, capsys):
    config = {"all": [dotfile.path]}
    touch_dotrc(source_dir, config)

    link(dotfile)
    assert not conflicts(dotfile)

    other_file = source_dir / "otherfile"
    other_file.touch()

    dotfile.target.unlink()
    dotfile.target.symlink_to(other_file)
    assert conflicts(dotfile)


def test_linked(source_dir, target_dir, dotfile):
    config = {"all": [dotfile.path]}
    touch_dotrc(source_dir, config)

    assert not linked(dotfile)

    link(dotfile)
    assert linked(dotfile)


def test_link(dotfile):
    dotfile.source.touch()

    def correctly_created(df: Dotfile) -> bool:
        return exists(df) and linked(df) and not conflicts(df)

    assert not correctly_created(dotfile)
    link(dotfile)
    assert correctly_created(dotfile)
