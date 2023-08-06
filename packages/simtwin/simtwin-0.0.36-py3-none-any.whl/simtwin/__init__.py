# pylint: disable-all
"""
Quirk to guarantee correct Pythonpath and single source of truth versioning
"""
from importlib.metadata import version, PackageNotFoundError
__author__ = """Henrik Stromberg"""
__email__ = 'henrik@askdrq.com'
try:
    __version__ = version('simtwin')
except PackageNotFoundError:
    __version__ = '0.0.0'

from . import broker  # noqa
from . import geometry  # noqa
from . import mesh  # noqa
from . import server  # noqa
from . import simulation  # noqa
