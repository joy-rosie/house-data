import logging
import sys
from typing import Optional

from .typing import TypePathLike
from .config import get_path_log

__all__ = [
    "get_logger",
]


LOGGING_FORMATTER = logging.Formatter(
    fmt=(
        "%(asctime)s.%(msecs)03d %(levelname)s "
        "%(module)s - %(funcName)s: %(message)s"
    ),
    datefmt="%Y-%m-%d %H:%M:%S",
)


def get_logger(
    key: str,
    path_log: Optional[TypePathLike],
) -> logging.Logger:

    path_log = get_path_log(path=path_log)

    logger = logging.Logger(key)

    path_log_file = path_log.joinpath(f"{key}.log")
    path_log_file.parent.mkdir(parents=True, exist_ok=True)

    file_handler = logging.FileHandler(path_log_file, mode="a")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(LOGGING_FORMATTER)

    console_handler = logging.StreamHandler(stream=sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(LOGGING_FORMATTER)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
