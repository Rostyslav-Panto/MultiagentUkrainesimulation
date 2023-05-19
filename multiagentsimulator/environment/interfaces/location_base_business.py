from abc import ABCMeta
from typing import cast, Tuple, Type, TypeVar, ClassVar

from .ids import PersonID
from .location_base import BaseLocation
from .location_rules import LocationRule, BusinessLocationRule, NonEssentialBusinessLocationRule
from .location_states import BusinessLocationState, NonEssentialBusinessLocationState
from .pandemic_types import DEFAULT
from .simulation_time import SimulationTime, SimulationTimeTuple


_BusinessState = TypeVar('_BusinessState', bound=BusinessLocationState)
_NonEssentialBusinessState = TypeVar('_NonEssentialBusinessState', bound=NonEssentialBusinessLocationState)


class BusinessBaseLocation(BaseLocation[_BusinessState], metaclass=ABCMeta):
    """Class that implements a base business location that has finite open hours."""

    location_rule_type: Type = BusinessLocationRule

    def sync(self, sim_time: SimulationTime) -> None:
        super().sync(sim_time)
        self._state.is_open = sim_time in self._state.open_time

    def update_rules(self, new_rule: LocationRule) -> None:
        super().update_rules(new_rule)
        rule = cast(BusinessLocationRule, new_rule)

        if rule.open_time is not None:
            self._state.open_time = (self._init_state.open_time if rule.open_time == DEFAULT
                                     else cast(SimulationTimeTuple, rule.open_time))

    def get_worker_work_time(self) -> SimulationTimeTuple:
        """Returns work-time for a new worker to work at the location. For example, a location that is open 24x7
        can return a shift slot of 8 hours, such that, there is a worker
        working at all times while the location is open. By default, work_time is set equal to open_time. Subclasses
        can modify to implement location-specific versions."""
        return self.state.open_time


class ImportantBusinessBaseLocation(BusinessBaseLocation[_BusinessState], metaclass=ABCMeta):
    """Class that implements an essential business location that has finite open hours."""
    pass


class NoImportantBusinessBaseLocation(BusinessBaseLocation[_NonEssentialBusinessState], metaclass=ABCMeta):
    """Class that implements a non essential base business location that has finite open hours."""

    location_rule_type: Type = NonEssentialBusinessLocationRule

    def sync(self, sim_time: SimulationTime) -> None:
        super().sync(sim_time)
        self._state.is_open = False if self._state.locked else sim_time in self._state.open_time

    def update_rules(self, new_rule: LocationRule) -> None:
        super().update_rules(new_rule)
        rule = cast(NonEssentialBusinessLocationRule, new_rule)

        if rule.lock is not None:
            self._state.locked = rule.lock


class AgeRestrictedBusinessBaseLocation(NoImportantBusinessBaseLocation[_NonEssentialBusinessState],
                                        metaclass=ABCMeta):
    """Class that implements a base age-restricted business location."""

    age_limits: ClassVar[Tuple[int, int]]

    def is_entry_allowed(self, person_id: PersonID) -> bool:
        if self.age_limits[0] <= person_id.age <= self.age_limits[1]:
            return super().is_entry_allowed(person_id)

        return False
