from abc import ABCMeta
from typing import cast, Tuple, Type, TypeVar, ClassVar

from .ids import PersonID
from .location_base import BaseLocation
from .location_rules import LocationRule, BusinessLocationRule, NonEssentialBusinessLocationRule
from .location_states import BusinessLocationState, NonEssentialBusinessLocationState
from .pandemic_types import DEFAULT
from .simulation_time import SimulationTime, SimulationTimeTuple


_BusinessState = TypeVar('_BusinessState', bound=BusinessLocationState)
_UnnecessaryBusinessState = TypeVar('_UnnecessaryBusinessState', bound=NonEssentialBusinessLocationState)


class BusinessBaseLocation(BaseLocation[_BusinessState], metaclass=ABCMeta):
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
        return self.state.open_time


class NecessaryBusinessBaseLocation(BusinessBaseLocation[_BusinessState], metaclass=ABCMeta):
    pass


class UnnecessaryBusinessBaseLocation(BusinessBaseLocation[_UnnecessaryBusinessState], metaclass=ABCMeta):
    location_rule_type: Type = NonEssentialBusinessLocationRule

    def sync(self, sim_time: SimulationTime) -> None:
        super().sync(sim_time)
        self._state.is_open = False if self._state.locked else sim_time in self._state.open_time

    def update_rules(self, new_rule: LocationRule) -> None:
        super().update_rules(new_rule)
        rule = cast(NonEssentialBusinessLocationRule, new_rule)

        if rule.lock is not None:
            self._state.locked = rule.lock


class AgeRestrictedBusinessBaseLocation(UnnecessaryBusinessBaseLocation[_UnnecessaryBusinessState],
                                        metaclass=ABCMeta):
    age_limit: ClassVar[Tuple[int, int]]

    def is_entry_allowed(self, person_id: PersonID) -> bool:
        if self.age_limit[0] <= person_id.age <= self.age_limit[1]:
            return super().is_entry_allowed(person_id)

        return False
