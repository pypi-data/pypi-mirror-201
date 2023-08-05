import os
from functools import lru_cache
from pathlib import Path

import yaml
from pydantic import BaseSettings, FilePath


class Settings(BaseSettings):
    notebooks_root_path: Path
    identity_path: FilePath = Path("~/.ssh/id_ed25519").expanduser()
    recipient_path: FilePath = Path("~/.ssh/id_ed25519.pub").expanduser()

    class Config:
        env_prefix = "halig_"


@lru_cache
def load_from_file(file_path: Path | None = None) -> Settings:
    if file_path is None:
        xdg_config_home = Path(os.getenv("XDG_CONFIG_HOME", "~/.config")).expanduser()
        if not xdg_config_home.exists():
            err = f"File {xdg_config_home} does not exist"
            raise FileNotFoundError(err)

        file_path = xdg_config_home / "halig" / "halig.yml"
        file_path.touch(exist_ok=True)
    elif not file_path.exists():
        err = f"File {file_path} does not exist"
        raise FileNotFoundError(err)

    with file_path.open("r") as f:
        data = yaml.safe_load(f)
    if not data:
        err = f"File {file_path} is empty"
        raise ValueError(err)
    return Settings(**data)
