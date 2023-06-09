
from orderedset import OrderedSet
from typing import Dict, FrozenSet, List, Mapping, Set

import numpy as np

from ..interfaces import ContactTracer, PersonID


class MaxSlotContactTracer(ContactTracer):
    """A max slot contact tracing app. In this app, contacts are discarded after the maximum storage slots are reached.
    For example, if storage_slots is 5, and the time_slot_scale is 24 (a day), only the last 5 days of contacts
    will be kept. Note that time_slot_scale is only used as a scale and it should be care of the user to
    make sure that the contacts are added in a proper way (respecting that scale)."""

    _storage_slots: int
    _time_slot_scale: int
    _memory: List[Dict[FrozenSet[PersonID], int]]
    _indices: List[Dict[PersonID, Set[FrozenSet[PersonID]]]]

    def __init__(self, storage_slots: int = 5, time_slot_scale: int = 24):
        self._storage_slots = storage_slots
        self._time_slot_scale = time_slot_scale
        self._memory = [dict() for i in range(0, storage_slots)]
        self._indices = [dict() for i in range(0, storage_slots)]

    def new_time_slot(self) -> None:
        self._memory = np.roll(self._memory, 1)
        self._indices = np.roll(self._indices, 1)
        self._memory[0] = dict()
        self._indices[0] = dict()

    def reset(self) -> None:
        self._memory = [dict() for i in range(0, self._storage_slots)]
        self._indices = [dict() for i in range(0, self._storage_slots)]

    def add_contacts(self, contacts: OrderedSet) -> None:
        for c in contacts:
            idx = frozenset(c)

            if idx not in self._memory[0]:
                self._memory[0][idx] = 0

            self._memory[0][idx] += 1

            for pid in idx:
                if pid not in self._indices[0]:
                    self._indices[0][pid] = OrderedSet()
                self._indices[0][pid].add(idx)

    def get_contacts(self, person_id: PersonID) -> Mapping[PersonID, np.ndarray]:
        res = dict()

        for slot_num, indices in enumerate(self._memory):
            if person_id not in self._indices[slot_num]:
                continue

            p_indices = self._indices[slot_num][person_id]

            for idx in p_indices:
                pid = [val for val in idx if val != person_id]
                if pid[0] not in res:
                    res[pid[0]] = np.zeros(self._storage_slots)
                res[pid[0]][slot_num] += self._memory[slot_num][idx]/float(self._time_slot_scale)

        return res
