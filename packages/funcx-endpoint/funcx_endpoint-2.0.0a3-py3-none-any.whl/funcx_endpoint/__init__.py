import warnings

from funcx_endpoint.version import DEPRECATION_FUNCX_ENDPOINT
from funcx_endpoint.version import __version__ as _version

__author__ = "The Globus Compute Team"
__version__ = _version

warnings.warn(DEPRECATION_FUNCX_ENDPOINT)
