import abc
from typing import Protocol


class Mutable(Protocol):
    """Provides `mute` method."""

    def mute(self, host: str) -> None:
        """Mute system audio on host."""


class VolumeControl(abc.ABC):
    @abc.abstractmethod
    def mute(
        self,
        host: str,
    ) -> None:
        """Mute system audio on host."""
        raise NotImplementedError
