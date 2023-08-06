"""Test shtab."""
import os
import shutil
from pathlib import Path

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

    def test_shtab(self, tmp_path: Path) -> None:
        """Test shtab. Check src.

        :param tmp_path:
        :type tmp_path: Path
        :rtype: None
        """
        os.chdir(tmp_path)
        copy("src/pyproject.toml")
        os.makedirs("src")
        copy("src/demo_shtab.py", "src")
        generate()
        for file in list(os.walk("sdist"))[0][-1]:
            with open(os.path.join("sdist", file)) as f:
                rst = f.read()
            assert rst != ""

    def test_typo(self, tmp_path: Path, caplog) -> None:
        """Test typo.

        :param tmp_path:
        :type tmp_path: Path
        :param caplog:
        :rtype: None
        """
        os.chdir(tmp_path)
        copy("typo/pyproject.toml")
        os.makedirs("src")
        copy("src/demo_shtab.py", "src")
        generate()
        assert (
            caplog.records[-1].message == "demo_shtab:shtab cannot be called!"
        )

    def test_shtab_is_not_installed(self, tmp_path: Path, caplog) -> None:
        """Test shtab is not installed.

        :param tmp_path:
        :type tmp_path: Path
        :param caplog:
        :rtype: None
        """
        os.chdir(tmp_path)
        copy("wrong/pyproject.toml")
        os.makedirs("src")
        copy("wrong/no_shtab.py", "src")
        generate()
        assert caplog.records[1].message == "No --print-completion found!"
