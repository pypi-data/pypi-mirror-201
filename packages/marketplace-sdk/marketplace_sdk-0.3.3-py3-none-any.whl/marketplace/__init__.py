#!/usr/bin/env python

"""Software Development Toolkit to communicate with the Materials MarketPlace
platform.

.. currentmodule:: marketplace
.. moduleauthor:: Carl Simon Adorf <simon.adorf@epfl.ch>
"""

from .client import MarketPlaceClient
from .version import __version__

__all__ = [
    "MarketPlaceClient",
    "__version__",
]
