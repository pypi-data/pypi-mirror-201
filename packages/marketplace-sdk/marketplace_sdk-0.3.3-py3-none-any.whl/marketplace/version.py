#!/usr/bin/env python

"""This module contains project version information.

.. currentmodule:: marketplace.version
.. moduleauthor:: Carl Simon Adorf <simon.adorf@epfl.ch>
"""

try:
    from dunamai import Version, get_version

    __version__ = Version.from_git().serialize()
except RuntimeError:
    __version__ = get_version("marketplace-sdk").serialize()
except ImportError:
    __version__ = "v0.3.3"
