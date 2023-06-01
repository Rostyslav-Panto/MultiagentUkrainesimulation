from abc import ABC, abstractmethod
from typing import Any

from .regulation import ChosenRegulation
from .simulation_state import SimulationState


class SimulationStateConsumer(ABC):

    @abstractmethod
    def consume_begin(self, sim_state: SimulationState) -> None:
        pass

    @abstractmethod
    def consume_state(self, sim_state: SimulationState, regulation: ChosenRegulation) -> None:
        pass

    @abstractmethod
    def finalize(self, *args: Any, **kwargs: Any) -> Any:

        pass

    @abstractmethod
    def reset(self) -> None:
        pass
    def close(self) -> None:
        pass
