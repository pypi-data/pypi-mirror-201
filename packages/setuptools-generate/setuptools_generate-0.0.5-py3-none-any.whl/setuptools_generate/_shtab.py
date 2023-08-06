"""shtab
========
"""
import logging
import os
import sys
from typing import Callable

from .utils import get_stdout

logger = logging.getLogger(__name__)


def generate_complete(function: Callable, prog: str, resources: str) -> None:
    """Generate complete.

    :param function:
    :type function: Callable
    :param prog:
    :type prog: str
    :param resources:
    :type resources: str
    :rtype: None
    """
    shells = {"bash": prog, "zsh": "_" + prog, "tcsh": prog + ".csh"}
    argv = sys.argv
    for shell, filename in shells.items():
        sys.argv = [prog, "--print-completion", shell]
        content = get_stdout(function).replace("\r\n", "\n")
        if content == "":
            logger.error("No --print-completion found!")
            return
        with open(os.path.join(resources, filename), "w", newline="") as f:
            f.write(content)
    sys.argv = argv
