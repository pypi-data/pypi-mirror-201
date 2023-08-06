"""Metainfo
===========
"""
import logging
from datetime import datetime
from pathlib import Path

from jinja2 import Template
from jinja2.exceptions import UndefinedError

logger = logging.getLogger(__name__)
TEMPLATE_FILE = str(
    Path(__file__).absolute().parent / "assets" / "jinja2" / "metainfo.py.j2"
)


def generate_metainfo(write_to: str, data: dict) -> None:
    """Generate metainfo.

    :param write_to:
    :type write_to: str
    :param data:
    :type data: dict
    :rtype: None
    """
    template = ""
    try:
        metainfo_template: dict[str, str] = data["tool"][
            "setuptools-generate"
        ]["metainfo-template"]
        if file := metainfo_template.get("file"):
            with open(file) as f:
                template = f.read()
        elif text := metainfo_template.get("text"):
            template = text
        else:
            logger.info("metainfo-template is incorrect, use default!")
    except KeyError:
        logger.info("metainfo-template doesn't exist, use default!")
    if template == "":
        with open(TEMPLATE_FILE) as f:
            template = f.read()
    try:
        content = Template(template).render(
            data=data, year=str(datetime.now().year)
        )
    except UndefinedError as e:
        logger.error("Undefind error!")
        raise e
    with open(write_to, "w") as f:
        f.write(content)
