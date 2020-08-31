from pathlib import Path

import pytest

from dotm.conftest import touch_dotrc
from dotm.dotfile import Dotfile
from dotm.main import dotm, get_relevant_files, path_to_dotfile


@pytest.mark.parametrize(
    "config,file_paths,hostname",
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
def test_relevant_files(mocker, config, file_paths, hostname):
    mocker.patch("dotm.main.gethostname", return_value=hostname)
    assert set(get_relevant_files(config)) == file_paths


@pytest.mark.parametrize(
    "path,source_directory,target_directory,expected_dotfile",
    [
        (
            ".emacs",
            Path("/source"),
            Path("/target"),
            Dotfile(".emacs", Path("/source/.emacs"), Path("/target/.emacs")),
        ),
        (
            ".emacs -> /tmp/.emacs",
            Path("/source"),
            Path("/target"),
            Dotfile(".emacs", Path("/source/.emacs"), Path("/tmp/.emacs")),
        ),
    ],
)
def test_path_to_dotfile(path, source_directory, target_directory, expected_dotfile):
    df = path_to_dotfile(path, source_directory, target_directory)
    assert df.path == expected_dotfile.path
    assert df.source == expected_dotfile.source
    assert df.target == expected_dotfile.target


def test_no_relevant_files(capsys, source_directory, target_directory):
    config = {}
    with pytest.raises(SystemExit) as e:
        dotm(config, source_directory, target_directory)

    assert e.value.code == 1
    captured = capsys.readouterr()
    assert "There are no files matching the host" in captured.out


# TODO Introduce a couple more integration tests
def test_dotm(mocker, source_directory, target_directory):
    config = {"all": [".emacs"], "host1": [".bashrc"], "host2": [".zshrc"]}
    touch_dotrc(source_directory, config)

    mocker.patch("dotm.main.gethostname", return_value="host1")
    existing, created = dotm(config, source_directory, target_directory)

    assert [df.path for df in created] == [".emacs", ".bashrc"]
    assert existing == []
