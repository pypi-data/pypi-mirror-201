import warnings

from globus_compute_endpoint.executors import HighThroughputExecutor
from globus_compute_endpoint.version import DEPRECATION_FUNCX_ENDPOINT

__all__ = ["HighThroughputExecutor"]

warnings.warn(DEPRECATION_FUNCX_ENDPOINT)
