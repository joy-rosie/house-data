import json
import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv

from .typing import TypePathLike


__all__ = [
    "load",
    "get_path_log",
    "get_path_data",
    "get_all_keys",
    "get_key_for_name",
    "get_path_data_for_key",
]


PATH_LOG = "PATH_LOG"
PATH_DATA = "PATH_DATA"
PATH_KEYS = "PATH_KEYS"


def load(
    path_env: Optional[TypePathLike] = None,
    override: Optional[bool] = None,
) -> bool:
    return load_dotenv(path_env, override=override)


def get_path_log(path: Optional[TypePathLike] = None) -> Path:
    if path is None:
        path = os.environ[PATH_LOG]
    return Path(path)


def get_path_data(path: Optional[TypePathLike] = None) -> Path:
    if path is None:
        path = os.environ[PATH_DATA]
    return Path(path)


def get_all_keys(path: Optional[TypePathLike] = None) -> dict[str, str]:
    if path is None:
        path = os.environ[PATH_KEYS]
    path = Path(path)
    keys = json.loads(path.read_text())
    return keys


def get_key_for_name(
    name: str,
    path_keys: Optional[TypePathLike] = None,
) -> str:
    return get_all_keys(path=path_keys)[name]


def get_path_data_for_key(
    key: str,
    path_data: Optional[TypePathLike],
) -> Path:
    path = Path(get_path_data(path=path_data)).joinpath(key)
    path.mkdir(parents=True, exist_ok=True)
    return path
