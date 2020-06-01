from pathlib import Path

import pytest

from dotm.conftest import touch_dotrc
from dotm.main import Dotfile, link, load_config, relevant_files, to_dotfile


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
    mocker.patch("dotm.main.gethostname", return_value="host1")

    link(dotrc, source_dir, dest_dir)

    for f in files:
        p = Path(f"{dest_dir}/{f}")
        assert p.is_symlink()
        assert p.resolve(f"{source_dir}/{f}")


def test_existing_dotfile_link(source_dir, dest_dir):
    dotfile = ".emacs"
    dotrc = {"all": [dotfile]}
    touch_dotrc(source_dir, dotrc)

    # Ensure the link exists
    source_file = source_dir / dotfile
    link_target = dest_dir / dotfile
    link_target.symlink_to(source_file)

    existing, missing = link(dotrc, source_dir, dest_dir)
    assert len(existing) == 1
    assert len(missing) == 0


def test_existing_dotfile_file(source_dir, dest_dir, capsys):
    """Ensure that dotm will not override existing files which are not symlinks."""
    dotfile = ".emacs"
    dotrc = {"all": [dotfile]}
    touch_dotrc(source_dir, dotrc)

    dotfile = Path(dest_dir, dotfile)
    dotfile.touch()

    with pytest.raises(SystemExit) as we:
        link(dotrc, source_dir, dest_dir)
        assert we.value.code == 1

    captured = capsys.readouterr()
    assert "Please resolve the conflict manually!" in captured.out


def test_missing_dotfile_target(source_dir, dest_dir):
    dotrc = {"all": [".emacs"]}
    touch_dotrc(source_dir, dotrc)

    existing, created = link(dotrc, source_dir, dest_dir)
    assert len(created) == 1
    assert len(existing) == 0


@pytest.mark.parametrize(
    "dotrc,file_paths,hostname",
    [
        # Straight forward with "all" block
        (
            {"all": [".emacs"], "host1": [".tmux.conf"], "otherhost": [".vimrc"]},
            {".emacs", ".tmux.conf"},
            "host1",
        ),
        # Multi host block
        ({"host1|host2|host3": [".emacs"]}, {".emacs"}, "host1"),
    ],
)
def test_relevant_files(mocker, dotrc, file_paths, hostname):
    mocker.patch("dotm.main.gethostname", return_value=hostname)
    assert set(relevant_files(dotrc)) == file_paths


def test_no_relevant_files(capsys):
    with pytest.raises(SystemExit) as e:
        relevant_files({})
        assert e.value.code == 1

    captured = capsys.readouterr()
    assert "There are no files matching the host" in captured.out


@pytest.mark.parametrize(
    "path,dotfile",
    [
        (
            ".emacs",
            Dotfile(
                source=Path("/home/user/dotfiles/.emacs"),
                target=Path("/home/user/.emacs"),
                name=".emacs",
            ),
        ),
        (
            "host-configuration.nix -> /etc/nixos/hostname.nix",
            Dotfile(
                source=Path("/home/user/dotfiles/host-configuration.nix"),
                target=Path("/etc/nixos/hostname.nix"),
                name="host-configuration.nix",
            ),
        ),
    ],
)
def test_to_dotfile(mocker, path, dotfile):
    source_dir = "/home/user/dotfiles"
    target_dir = "/home/user"
    mocker.patch("dotm.main.Path.cwd", return_value=Path(source_dir))
    mocker.patch("dotm.main.Path.home", return_value=Path(target_dir))
    assert to_dotfile(path, source_dir, target_dir) == dotfile
