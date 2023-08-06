r"""Test changelog"""
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

    def test_empty_changelog(self, tmp_path: Path, caplog) -> None:
        """Test empty changelog.

        :param tmp_path:
        :type tmp_path: Path
        :param caplog:
        :rtype: None
        """
        os.chdir(tmp_path)
        copy("pyproject.toml")
        with open("CHANGELOG.md", "w") as f:
            f.write("")
        generate()
        assert (
            caplog.records[1].message == "No correct changelog content, skip!"
        )

    def test_changelog(self, tmp_path: Path) -> None:
        """Test changelog.

        :param tmp_path:
        :type tmp_path: Path
        :rtype: None
        """
        os.chdir(tmp_path)
        copy("pyproject.toml")
        copy("CHANGELOG.md")
        generate()
        with open(
            os.path.join(os.path.join(HERE, "test"), "CHANGELOG.md")
        ) as f:
            expected = f.read().strip()
        with open(os.path.join("build", "CHANGELOG.md")) as f:
            result = f.read()
        assert expected == result
