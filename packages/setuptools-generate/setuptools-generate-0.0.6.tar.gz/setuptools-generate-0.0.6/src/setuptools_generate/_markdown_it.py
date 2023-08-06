r"""Markdown it
===============
"""
import logging
import os

from markdown_it import MarkdownIt

logger = logging.getLogger(__name__)
md = MarkdownIt("commonmark")


def generate_changelog(build: str, fname: str) -> None:
    """Generate changelog.

    :param build:
    :type build: str
    :param fname
    :type fname: str
    :rtype: None
    """
    with open(fname) as f:
        input = f.read()
    tokens = []
    number = 0
    for token in md.parse(input):
        if number == 2:
            tokens += [token]
        if number == 3:
            tokens.pop()
            break
        if token.tag == "h2":
            number += 1
    if tokens == []:
        logger.warning("No correct changelog content, skip!")
        return None
    output = md.renderer.render(tokens, md.options, {}).strip()
    with open(os.path.join(build, fname), "w") as f:
        f.write(output)
