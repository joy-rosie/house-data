import logging
from pathlib import Path
import sys
from typing import Optional

from .typing import TypePathLike

__all__ = [
    'get_logger',
]


LOGGING_FORMATTER = logging.Formatter(
    fmt='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)


def get_logger(
    key: str,
    path_log: Optional[TypePathLike],
) -> logging.Logger:

    path_log = Path(path_log)

    logger = logging.Logger(key)

    file_handler = logging.FileHandler(path_log.joinpath(f'{key}.log'), mode='w')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(LOGGING_FORMATTER)

    console_handler = logging.StreamHandler(stream=sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(LOGGING_FORMATTER)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
