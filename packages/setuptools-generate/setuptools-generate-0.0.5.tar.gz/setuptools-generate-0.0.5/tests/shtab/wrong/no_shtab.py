"""Test shtab."""
from argparse import ArgumentParser


def get_parser() -> ArgumentParser:
    """Get parser.

    :rtype: ArgumentParser
    """
    parser = ArgumentParser("test")
    return parser


def main():
    """Run."""
    parser = get_parser()
    parser.parse_args()
