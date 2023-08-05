"""
A module implementing a configuration interface for the package.
"""

# third-party
from vcorelib.dict.codec import BasicDictCodec as _BasicDictCodec

# internal
from rcmpy.schemas import RcmpyDictCodec as _RcmpyDictCodec


class Config(_RcmpyDictCodec, _BasicDictCodec):
    """The top-level configuration object for the package."""
