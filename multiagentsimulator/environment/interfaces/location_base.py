from abc import ABCMeta
from copy import deepcopy
from typing import Optional, cast, TypeVar, Union
from uuid import uuid4

import numpy as np

from . import globals
from .ids import PersonID, LocationID
from .location import Location
from .location_rules import LocationRule
from .location_states import LocationState, ContactRate
from .pandemic_types import DEFAULT
from .registry import Registry
from .simulation_time import SimulationTime, SimulationTimeTuple


_State = TypeVar('_State', bound=LocationState)


class BaseLocation(Location[_State], metaclass=ABCMeta):
    location_rule_type = LocationRule

    _id: LocationID
    _init_state: _State
    _state: _State
    _registry: Registry
    _numpy_rng: np.random.RandomState
    _current_sim_time: SimulationTime

    def __init__(self, loc_id: Union[str, LocationID, None] = None, init_state: Optional[_State] = None, position=None):

        assert globals.registry, 'No registry found. Create the repo wide registry first by calling init_globals()'
        self._registry = globals.registry
        self._numpy_rng = globals.numpy_rng

        if loc_id is None:
            self._id = LocationID(type(self).__name__ + str(uuid4()))
        else:
            self._id = LocationID(loc_id) if isinstance(loc_id, str) else loc_id
        self._init_state = init_state or self.state_type()

        self._state = deepcopy(self._init_state)
        self._registry.register_location(self)
        self.position = position

    @property
    def id(self) -> LocationID:
        return self._id

    @property
    def init_state(self) -> _State:
        return self._init_state

    @property
    def state(self) -> _State:
        return self._state

    def sync(self, sim_time: SimulationTime) -> None:
        self._current_sim_time = sim_time

    def update_rules(self, new_rule: LocationRule) -> None:
        cr = new_rule.contact_rate
        if cr is not None:
            self._state.contact_rate = (self._init_state.contact_rate if cr == DEFAULT else cast(ContactRate, cr))

        if new_rule.visitor_time is not None:
            self._state.visitor_time = (self._init_state.visitor_time if new_rule.visitor_time == DEFAULT
                                        else cast(SimulationTimeTuple, new_rule.visitor_time))
        if new_rule.visitor_capacity is not None:
            self._state.visitor_capacity = (self._init_state.visitor_capacity if new_rule.visitor_capacity == DEFAULT
                                            else new_rule.visitor_capacity)

    def is_entry_allowed(self, person_id: PersonID) -> bool:
        allow_assignee = person_id in self._state.assignees

        allow_visitor = (self._current_sim_time in self._state.visitor_time and
                         (self._state.visitor_capacity == -1 or
                          len(self._state.visitors_in_location) < self._state.visitor_capacity))

        return self._state.is_open and (allow_assignee or allow_visitor)

    def assign_person(self, person_id: PersonID) -> None:
        self._state.assignees.add(person_id)

    def add_person_to_location(self, person_id: PersonID) -> None:
        if person_id in self._state.assignees:
            self._state.assignees_in_location.add(person_id)
        else:
            self._state.visitors_in_location.add(person_id)

    def remove_person_from_location(self, person_id: PersonID) -> None:
        if person_id in self._state.assignees_in_location:
            self._state.assignees_in_location.remove(person_id)
        elif person_id in self._state.visitors_in_location:
            self._state.visitors_in_location.remove(person_id)
        else:
            # person is not in location
            pass

    def reset(self) -> None:
        self._state = deepcopy(self._init_state)
