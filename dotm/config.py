from pathlib import Path
from typing import Dict

import yaml


def load_config(source_directory: Path) -> Dict:
    """Load .dotrc file from source directory."""
    config_file = source_directory / ".dotrc"

    if not config_file.is_file():
        print("Source directory does not contain a .dotrc file")
        exit(1)

    with config_file.open() as f:
        try:
            return yaml.load(f, Loader=yaml.BaseLoader)
        except yaml.YAMLError:
            print(".dotrc is invalid")
            exit(1)
