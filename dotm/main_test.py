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


def test_no_relevant_files(source_dir, target_dir, capsys, mocker):
    mocker.patch("dotm.main.gethostname", return_value="host")

    with pytest.raises(SystemExit) as excinfo:
        dotm({}, source_dir, target_dir)

    stderr = capsys.readouterr().out
    assert 'No files matching host "host"' in stderr
    assert excinfo.value.code == 1


# TODO Introduce a couple more integration tests
def test_dotm(mocker, source_dir, target_dir):
    cfg = {
        "all": [
            Dotfile(
                name=".emacs",
                source=source_dir / ".emacs",
                target=target_dir / ".emacs",
            )
        ],
        "host1": [
            Dotfile(
                name=".bashrc",
                source=source_dir / ".bashrc",
                target=target_dir / ".bashrc",
            )
        ],
        "host2": [
            Dotfile(
                name=".zshrc",
                source=source_dir / ".zshrc",
                target=target_dir / ".zshrc",
            )
        ],
    }
    touch_dotrc(source_dir, cfg)

    mocker.patch("dotm.main.gethostname", return_value="host1")
    existing, created = dotm(cfg, source_dir, target_dir)

    assert [df.name for df in created] == [".emacs", ".bashrc"]
    assert existing == []
