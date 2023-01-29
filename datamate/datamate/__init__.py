import warnings

from . import logging  # noqa: F401
from . import typing  # noqa: F401
from . import config

try:
    config.load(".env")
except:
    warnings.warn("Could not load config when importing datamate")
