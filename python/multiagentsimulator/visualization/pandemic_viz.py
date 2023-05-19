from abc import ABC, abstractmethod
from typing import Any


class PandemicViz(ABC):
    """An interface for simulator visualization"""

    @abstractmethod
    def record(self, data: Any) -> None:
        """
        Record data to internals for plotting.

        :param data:
        """

    def plot(self, *args: Any, **kwargs: Any) -> None:
        """Make plots"""
