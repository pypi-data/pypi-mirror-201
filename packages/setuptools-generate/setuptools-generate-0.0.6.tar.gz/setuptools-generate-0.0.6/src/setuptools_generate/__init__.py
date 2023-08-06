"""Provide ``__version__`` for
`importlib.metadata.version() <https://docs.python.org/3/library/importlib.metadata.html#distribution-versions>`_.
"""
import logging
import os
import sys
from importlib import import_module
from typing import Callable

from click import BaseCommand
from setuptools import Distribution

from ._help2man import generate_man

try:
    from ._version import __version__, __version_tuple__  # type: ignore
except ImportError:
    __version__ = "rolling"
    __version_tuple__ = (0, 0, 0, __version__, "")

try:
    import tomllib  # type: ignore
except ImportError:
    import tomli as tomllib

logger = logging.getLogger(__name__)


def generate(distribution: Distribution | None = None) -> None:
    """Generate.

    :param distribution:
    :type distribution: Distribution | None
    :rtype: None
    """
    if not os.path.isfile("pyproject.toml"):
        logger.error("No pyproject.toml is found!")
        return
    with open("pyproject.toml", "rb") as f:
        data = tomllib.load(f)
    try:
        write_to: str = data["tool"]["setuptools-generate"]["write-to"]

        from .metainfo import generate_metainfo  # isort: skip

        generate_metainfo(write_to, data)
    except KeyError:
        logger.warning(
            "no [tool.setuptools-generate.write-to] in pyproject.toml, "
            "skip writing metainfo!"
        )
    cwd = os.getcwd()
    build = os.path.join(cwd, "build")
    sdist = os.path.join(cwd, "sdist")
    os.makedirs(build, exist_ok=True)
    os.makedirs(sdist, exist_ok=True)
    fname = "CHANGELOG.md"
    if os.path.exists(fname):
        from ._markdown_it import generate_changelog

        generate_changelog(build, fname)
    try:
        completions: dict[str, str] = data["project"]["scripts"]
    except KeyError:
        logger.warning("No [project.scripts] in your pyproject.toml!")
        return
    sys.path.insert(0, cwd)
    sys.path.insert(0, os.path.join(cwd, "src"))
    for prog, path in completions.items():
        module_path, _, function_name = path.rpartition(":")
        module = import_module(module_path)
        function = vars(module).get(function_name)
        if isinstance(function, BaseCommand):
            from ._click import generate_complete
        elif isinstance(function, Callable):
            from ._shtab import generate_complete
        else:
            logger.error(path + " cannot be called!")
            return

        generate_complete(function, prog, sdist)  # type: ignore
        generate_man(function, prog, sdist, build)
    sys.path.pop(0)
    sys.path.pop(0)
