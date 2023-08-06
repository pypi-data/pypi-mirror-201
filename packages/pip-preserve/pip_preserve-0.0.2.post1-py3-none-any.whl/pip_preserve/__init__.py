#!/usr/bin/env python3

"""Output installed Python packages in requirements format, including also hashes of Python packages."""

from ._lib import preserve_requirements

__version__ = "0.0.2.post1"
__author__ = "Fridolin Pokorny <fridolin.pokorny@gmail.com>"
__license__ = "BSD-3-Clause"
__title__ = "pip-preserve"

__all__ = [
    preserve_requirements.__name__,
]
