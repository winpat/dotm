import pytest

from dotm.conftest import touch_dotrc
from dotm.dotfile import Dotfile
from dotm.main import dotm, get_relevant_files


@pytest.mark.parametrize(
    "config,file_paths,hostname",
    [
        (
            {"all": [".emacs"], "host1": [".tmux.conf"], "otherhost": [".vimrc"]},
            {".emacs", ".tmux.conf"},
            "host1",
        ),
        ({"host1": [".emacs"]}, {".emacs"}, "host1"),
    ],
)
def test_relevant_files(mocker, config, file_paths, hostname):
    mocker.patch("dotm.main.gethostname", return_value=hostname)
    assert set(get_relevant_files(config)) == file_paths


def test_no_relevant_files(source_directory, target_directory, capsys, mocker):
    mocker.patch("dotm.main.gethostname", return_value="host")

    with pytest.raises(SystemExit) as excinfo:
        dotm({}, source_directory, target_directory)

    stderr = capsys.readouterr().out
    assert 'No files matching host "host"' in stderr
    assert excinfo.value.code == 1


# TODO Introduce a couple more integration tests
def test_dotm(mocker, source_directory, target_directory):
    cfg = {
        "all": [
            Dotfile(
                path=".emacs",
                source=source_directory / ".emacs",
                target=target_directory / ".emacs",
            )
        ],
        "host1": [
            Dotfile(
                path=".bashrc",
                source=source_directory / ".bashrc",
                target=target_directory / ".bashrc",
            )
        ],
        "host2": [
            Dotfile(
                path=".zshrc",
                source=source_directory / ".zshrc",
                target=target_directory / ".zshrc",
            )
        ],
    }
    touch_dotrc(source_directory, cfg)

    mocker.patch("dotm.main.gethostname", return_value="host1")
    existing, created = dotm(cfg, source_directory, target_directory)

    assert [df.path for df in created] == [".emacs", ".bashrc"]
    assert existing == []
