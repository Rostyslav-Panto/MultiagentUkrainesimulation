from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Type, Generic, TypeVar, ClassVar

from .ids import PersonID, LocationID
from .location_rules import LocationRule
from .location_states import LocationState
from .simulation_time import SimulationTime
from ...utils import abstract_class_property


class LocationError(Exception):
    pass


@dataclass(frozen=True)
class LocationSummary:

    entry_count: float = 0

    visitor_count: float = 0

_State = TypeVar('_State', bound=LocationState)


class Location(ABC, Generic[_State]):

    location_rule_type: Type = abstract_class_property()  # The type of the location rule used by the location
    state_type: ClassVar[Type[_State]]

    @property
    @abstractmethod
    def id(self) -> LocationID:
        pass

    @property
    @abstractmethod
    def state(self) -> _State:
        pass

    @property
    @abstractmethod
    def init_state(self) -> _State:
        pass

    @abstractmethod
    def sync(self, sim_time: SimulationTime) -> None:
        pass

    @abstractmethod
    def update_rules(self, new_rule: LocationRule) -> None:
        pass

    @abstractmethod
    def is_entry_allowed(self, person_id: PersonID) -> bool:
        pass

    @abstractmethod
    def assign_person(self, person_id: PersonID) -> None:
        pass

    @abstractmethod
    def add_person_to_location(self, person_id: PersonID) -> None:
        """Adds a person with the given ID to the location"""
        pass

    @abstractmethod
    def remove_person_from_location(self, person_id: PersonID) -> None:
        """Removes a person with the given ID from the location"""
        pass

    @abstractmethod
    def reset(self) -> None:
        """Reset location to its initial state."""
