import os
from functools import lru_cache
from pathlib import Path

import yaml
from pydantic import BaseSettings, DirectoryPath, FilePath


class Settings(BaseSettings):
    """Settings model. It mainly stores paths that are interesting to the project.
     All the path-attributes described below have a validity check upon instantiation,
     meaning that they should exist and be readable and/or writable

    Attributes:
        notebooks_root_path (DirectoryPath): a *valid* path to a directory that
            may contain notes or other notebooks
        identity_path (FilePath): a *valid* path to an identity file, which usually
            is understood as a private key. Defaults to `~/.ssh/id_ed25519`
        recipient_path (FilePath): a *valid* path to a recipient file, which usually
            is understood as a public key. Defaults to `~/.ssh/id_ed25519.pub`
    """

    notebooks_root_path: DirectoryPath
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
