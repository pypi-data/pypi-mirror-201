"""click
========
"""
import os

from click import BaseCommand
from click.shell_completion import get_completion_class


def generate_complete(command: BaseCommand, prog: str, resources: str) -> None:
    """Generate complete.

    :param command:
    :type command: BaseCommand
    :param prog:
    :type prog: str
    :param resources:
    :type resources: str
    :rtype: None
    """
    shells = {"bash": prog, "zsh": "_" + prog, "fish": prog + ".fish"}
    for shell, filename in shells.items():
        comp_cls = get_completion_class(shell)
        content = (
            comp_cls(  # type: ignore
                command, {}, prog, f"_{prog.upper()}_COMPLETE"
            )
            .source()
            .replace("\r\n", "\n")
        )
        with open(os.path.join(resources, filename), "w", newline="") as f:
            f.write(content)
