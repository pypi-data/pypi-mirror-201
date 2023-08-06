"""Utilities
============
"""
import io
from contextlib import redirect_stdout, suppress
from typing import Callable


def get_stdout(function: Callable) -> str:
    """Get stdout.

    :param function:
    :type function: Callable
    :rtype: str
    """
    string = io.StringIO()
    with redirect_stdout(string), suppress(SystemExit):
        function()
    string.seek(0)
    content = string.read()
    return content
