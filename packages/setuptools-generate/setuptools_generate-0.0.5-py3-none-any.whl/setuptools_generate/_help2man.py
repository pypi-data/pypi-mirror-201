"""help2man
===========
"""
import os
import sys
from typing import Callable

from help2man import TEMPLATES, help2man

from .utils import get_stdout


def generate_man(
    function: Callable, prog: str, resources: str, data: dict
) -> None:
    """Generate man.

    :param function:
    :type function: Callable
    :param prog:
    :type prog: str
    :param resources:
    :type resources: str
    :param data:
    :type data: dict
    :rtype: None
    """
    argv = sys.argv
    sys.argv = [prog, "--help"]
    helpstr = get_stdout(function)
    sys.argv = [prog, "--version"]
    versionstr = get_stdout(function)
    sys.argv = argv
    man = help2man(helpstr, versionstr)
    with open(os.path.join(resources, prog + ".1"), "w") as f:
        f.write(man)
    doc = help2man(helpstr, versionstr, template=TEMPLATES["markdown"])
    with open(os.path.join(resources, prog + ".1.md"), "w") as f:
        f.write(doc)
