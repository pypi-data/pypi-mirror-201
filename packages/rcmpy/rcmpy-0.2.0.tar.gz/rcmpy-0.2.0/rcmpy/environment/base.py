"""
A module implementing a basic environment interface.
"""

# built-in
from contextlib import ExitStack
from typing import Optional

# third-party
from vcorelib.io.types import FileExtension
from vcorelib.logging import LoggerMixin

# internal
from rcmpy import PKG_NAME
from rcmpy.config import Config
from rcmpy.state import State


class BaseEnvironment(LoggerMixin):
    """A class implementing this package's base runtime environment."""

    def __init__(self, state: State, stack: ExitStack) -> None:
        """Initialize this instance."""

        super().__init__()
        self.state = state
        self.stack = stack
        self._config: Optional[Config] = None

        config_base = state.directory.joinpath(PKG_NAME)

        config_candidates = list(
            FileExtension.data_candidates(config_base, exists_only=True)
        )

        if not config_candidates:
            self.logger.error(
                "No config found: %s.",
                list(
                    str(x) for x in FileExtension.data_candidates(config_base)
                ),
            )
        else:
            assert len(config_candidates) == 1, config_candidates
            self._config = Config.decode(config_candidates[0])
            self.logger.info("Loaded config '%s'.", config_candidates[0])
            self._init_loaded()

    def _init_loaded(self) -> None:
        """Called during initialization if a valid configuration is loaded."""

    @property
    def config_loaded(self) -> bool:
        """Determine if this environment has loaded a config."""
        return self._config is not None

    @property
    def config(self) -> Config:
        """Get this environment's configuration object."""
        assert self._config is not None, "Config not loaded!"
        return self._config
