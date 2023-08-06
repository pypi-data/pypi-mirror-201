"""Test."""
import os
from pathlib import Path

from setuptools_generate import generate  # type: ignore


class Test:
    """Test."""

    def test_dir_without_toml(self, tmp_path: Path, caplog) -> None:
        """Test dir without toml.

        :param tmp_path:
        :type tmp_path: Path
        :param caplog:
        :rtype: None
        """
        os.chdir(tmp_path)
        generate()
        assert caplog.records[-1].message == "No pyproject.toml is found!"

    def test_dir_with_empty_toml(self, tmp_path: Path, caplog) -> None:
        """Test dir with empty toml.

        :param tmp_path:
        :type tmp_path: Path
        :param caplog:
        :rtype: None
        """
        os.chdir(tmp_path)
        with open("pyproject.toml", "w") as f:
            f.write("")
        generate()
        assert (
            caplog.records[-1].message
            == "No [project.scripts] in your pyproject.toml!"
        )
