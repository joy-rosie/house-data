import json
from pathlib import Path
from typing import NoReturn, Optional

from dotenv import dotenv_values

from .typing import TypePathLike


__all__ = [
    'load',
    'get',
    'get_path_data',
    'get_path_log',
    'get_keys',
    'get_key',
]

config_env = None
config_keys = None


def load(path_env: TypePathLike) -> NoReturn:
    path_env = Path(path_env)
    config_env = dotenv_values(path_env)

    path_keys = config_env['PATH_KEYS']
    config_keys = json.load(path_keys)


def get() -> dict[str,dict[str, str]]:
    return dict(env=config_env, keys=config_keys)


def get_path_data() -> Path:
    return Path(config_env['PATH_DATA'])


def get_path_log(path: Optional[TypePathLike] = None) -> Path:
    if path is None:
        path = config_env['PATH_LOG']
    return Path(path)


def get_keys() -> dict[str, str]:
    return config_keys


def get_key(name: str) -> str:
    return config_keys[name]
