"""Test click."""
import os
import shutil
import sys
from pathlib import Path

import pytest

from setuptools_generate import generate  # type: ignore

HERE = os.path.dirname(__file__)


def copy(filename: str, target: str = ".") -> None:
    """Copy.

    :param filename:
    :type filename: str
    :param target:
    :type target: str
    :rtype: None
    """
    shutil.copy(os.path.join(HERE, filename), target)


class Test:
    """Test."""

    @pytest.mark.skipif(
        sys.platform == "win32",
        reason="bash is not installed in Windows be default",
    )
    def test_click(self, tmp_path: Path) -> None:
        """Test click. Check current directory.

        :param tmp_path:
        :type tmp_path: Path
        :rtype: None
        """
        os.chdir(tmp_path)
        copy("src/pyproject.toml")
        copy("src/demo_click.py")
        generate()
        for file in list(os.walk("sdist"))[0][-1]:
            with open(os.path.join("sdist", file)) as f:
                rst = f.read()
            assert rst != ""
