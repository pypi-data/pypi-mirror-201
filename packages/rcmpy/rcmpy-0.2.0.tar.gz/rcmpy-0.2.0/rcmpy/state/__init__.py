"""
A module implementing this package's stateful information that persists across
invocations.
"""

# built-in
from contextlib import contextmanager
from logging import getLogger
from pathlib import Path
from typing import Iterator, cast

# third-party
from vcorelib.dict.cache import FileCache
from vcorelib.io.types import JsonObject as _JsonObject
from vcorelib.paths import Pathlike, normalize

# internal
from rcmpy.paths import default_config_directory, default_state_directory
from rcmpy.schemas import RcmpyDictCodec as _RcmpyDictCodec

LOG = getLogger(__name__)


class State(_RcmpyDictCodec):
    """The top-level configuration object for the package."""

    directory: Path
    variant: str

    def init(self, data: _JsonObject) -> None:
        """Perform implementation-specific initialization."""

        self.logger = LOG

        self.directory = normalize(
            cast(str, data.get("directory", default_config_directory()))
        ).resolve()

        self.logger.info("Using directory '%s'.", self.directory)

        self.variant: str = cast(str, data["variant"])
        if self.variant:
            self.logger.info("Using variant '%s'.", self.variant)

    def set_directory(self, path: Pathlike) -> None:
        """Set a new directory to use as the data repository."""

        new_dir = normalize(path).resolve()

        if new_dir == self.directory:
            self.logger.info("New directory '%s' same as current.", new_dir)
            return

        self.directory = new_dir
        self.logger.info("Set directory to '%s'.", new_dir)

    def set_variant(self, variant: str = None) -> None:
        """Set a new variant value."""

        if not variant:
            self.logger.info("Current variant: '%s'.", self.variant)
        elif variant != self.variant:
            self.variant = variant
            self.logger.info("Updating variant to '%s'.", variant)

    def asdict(self) -> _JsonObject:
        """Obtain a dictionary representing this instance."""

        return {"directory": str(self.directory), "variant": self.variant}


@contextmanager
def load_state(
    root: Pathlike = None, name: str = "state.json"
) -> Iterator[State]:
    """This needs to be a context manager, so it get's written back to disk."""

    if root is None:
        root = default_state_directory()

    with FileCache(normalize(root, name)).loaded() as data:
        state = State.create(data, verify=False)
        yield state

        # Update the original dictionary with any changes to the state object.
        data.update(state.asdict())
