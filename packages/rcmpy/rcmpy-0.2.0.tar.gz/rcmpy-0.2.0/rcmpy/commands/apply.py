"""
An entry-point for the 'apply' command.
"""

# built-in
from argparse import ArgumentParser as _ArgumentParser
from argparse import Namespace as _Namespace

# third-party
from vcorelib.args import CommandFunction as _CommandFunction

# internal
from rcmpy.environment import load_environment


def apply_cmd(_: _Namespace) -> int:
    """Execute the apply command."""

    with load_environment() as env:
        if not env.config_loaded:
            return 1

        print(env.config)

    return 0


def add_apply_cmd(_: _ArgumentParser) -> _CommandFunction:
    """Add apply-command arguments to its parser."""

    return apply_cmd
