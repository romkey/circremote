# SPDX-FileCopyrightText: 2025 John Romkey
#
# SPDX-License-Identifier: MIT

from .version import VERSION

__version__ = VERSION

class Error(Exception):
    """Base exception for circremote package."""
    pass 