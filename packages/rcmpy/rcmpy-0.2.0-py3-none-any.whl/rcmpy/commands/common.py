"""
A module for common argument-parsing methods.
"""

# built-in
from argparse import ArgumentParser as _ArgumentParser


def add_default_flag(parser: _ArgumentParser) -> None:
    """Adds a default-flag argument."""

    parser.add_argument(
        "-d",
        "--default",
        action="store_true",
        help="sets the directory back to the package default",
    )
