"""Test metainfo."""
import os
import shutil
from datetime import datetime
from pathlib import Path

import pytest

from setuptools_generate import generate  # type: ignore

now = datetime.now
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

    def test_empty_metainfo(self, tmp_path: Path, caplog) -> None:
        """Test empty metainfo.

        :param tmp_path:
        :type tmp_path: Path
        :param caplog:
        :rtype: None
        """
        os.chdir(tmp_path)
        copy("empty/pyproject.toml")
        with pytest.raises(Exception):
            generate()
        assert caplog.records[-1].message == "Undefind error!"

    def test_no_template_metainfo(self, tmp_path: Path) -> None:
        """Test no template metainfo.

        :param tmp_path:
        :type tmp_path: Path
        :rtype: None
        """
        os.chdir(tmp_path)
        copy("no_template/pyproject.toml")
        generate()
        with open("_metainfo.py") as f:
            rst = f.read()
        with open(
            os.path.join(os.path.join(HERE, "no_template"), "_metainfo.py")
        ) as f:
            expected = f.read().strip().replace("2022", now().strftime("%Y"))
        assert expected == rst

    def test_incorrect_template_metainfo(self, tmp_path: Path) -> None:
        """Test incorrect template metainfo.

        :param tmp_path:
        :type tmp_path: Path
        :rtype: None
        """
        os.chdir(tmp_path)
        copy("incorrect_template/pyproject.toml")
        generate()
        with open("_metainfo.py") as f:
            rst = f.read()
        with open(
            os.path.join(
                os.path.join(HERE, "incorrect_template"), "_metainfo.py"
            )
        ) as f:
            expected = f.read().strip().replace("2022", now().strftime("%Y"))
        assert expected == rst

    def test_template_file_metainfo(self, tmp_path: Path) -> None:
        """Test template file metainfo.

        :param tmp_path:
        :type tmp_path: Path
        :rtype: None
        """
        os.chdir(tmp_path)
        copy("template_file/pyproject.toml")
        copy("template_file/template.py")
        generate()
        with open("_metainfo.py") as f:
            rst = f.read()
        with open(
            os.path.join(os.path.join(HERE, "template_file"), "_metainfo.py")
        ) as f:
            expected = f.read().strip().replace("2022", now().strftime("%Y"))
        assert expected == rst

    def test_template_text_metainfo(self, tmp_path: Path) -> None:
        """Test template text metainfo.

        :param tmp_path:
        :type tmp_path: Path
        :rtype: None
        """
        os.chdir(tmp_path)
        copy("template_text/pyproject.toml")
        generate()
        with open("_metainfo.py") as f:
            rst = f.read()
        with open(
            os.path.join(os.path.join(HERE, "template_text"), "_metainfo.py")
        ) as f:
            expected = f.read().strip().replace("2022", now().strftime("%Y"))
        assert expected == rst
