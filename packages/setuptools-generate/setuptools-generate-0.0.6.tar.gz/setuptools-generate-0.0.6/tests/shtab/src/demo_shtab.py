"""Test shtab."""
from argparse import ArgumentParser

import shtab


def get_parser() -> ArgumentParser:
    """Get parser.

    :rtype: ArgumentParser
    """
    parser = ArgumentParser("test")
    shtab.add_argument_to(parser, preamble="# TEST")
    return parser


def main():
    """Run."""
    parser = get_parser()
    parser.parse_args()
