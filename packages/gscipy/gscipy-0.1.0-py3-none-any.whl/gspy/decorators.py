"""Module
"""
from __future__ import annotations

__author__ = "Matteo Gabba"
__copyright__ = "Copyright 2022, all right reserved Gabba Scientific"
__status__ = "Development"

from functools import wraps


def check_args_len(method):
    """Class-method decorator to assert length of two vector arguments (self, other)."""

    @wraps(method)
    def wrapped_method(self, other):
        method_name = method.__qualname__

        if isinstance(other, self.__class__):
            assert len(self) == len(other), (
                f"{method_name}(self, other): operand 'self' has different dimension"
                f" ({len(self)}) than operand 'other' ({len(other)})"
            )

        return method(self, other)

    return wrapped_method
