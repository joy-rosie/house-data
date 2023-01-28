import warnings

from . import logging
from . import typing
from . import config

try:
    config.load('.env')
except:
    warnings.warn('Could not load config when importing datamate')
