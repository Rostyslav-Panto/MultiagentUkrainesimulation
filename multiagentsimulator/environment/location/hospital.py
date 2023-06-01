
from dataclasses import dataclass, field
from typing import Set, cast

from .utils import get_work_time_for_24_7_open_locations
from ..interfaces import PersonID, InfectionSummary, BusinessLocationState, SimulationTimeTuple, BusinessBaseLocation


@dataclass
class HospitalState(BusinessLocationState):
    patient_capacity: int = -1

    patients_in_location: Set[PersonID] = field(default_factory=set, init=False)

    num_admitted_patients: int = field(init=False, default=0)

    open_time: SimulationTimeTuple = field(default_factory=SimulationTimeTuple, init=False)

    @property
    def persons_in_location(self) -> Set[PersonID]:
        persons = super().persons_in_location
        persons.union(self.patients_in_location)
        return persons


class Hospital(BusinessBaseLocation[HospitalState]):
    state_type = HospitalState

    def is_entry_allowed(self, person_id: PersonID) -> bool:
        inf_sum = self._registry.get_person_infection_summary(person_id)
        state = cast(HospitalState, self._state)

        allow_patient = (inf_sum == InfectionSummary.CRITICAL and
                         (state.patient_capacity == -1 or len(state.patients_in_location) < state.patient_capacity))

        return allow_patient or (inf_sum != InfectionSummary.CRITICAL and super().is_entry_allowed(person_id))

    def add_person_to_location(self, person_id: PersonID) -> None:
        inf_sum = self._registry.get_person_infection_summary(person_id)
        state = cast(HospitalState, self._state)
        if inf_sum == InfectionSummary.CRITICAL:
            state.patients_in_location.add(person_id)
            state.num_admitted_patients += 1
        else:
            super().add_person_to_location(person_id)

    def remove_person_from_location(self, person_id: PersonID) -> None:
        state = cast(HospitalState, self._state)
        if person_id in state.patients_in_location:
            state.patients_in_location.remove(person_id)
        else:
            super().remove_person_from_location(person_id)

    def get_worker_work_time(self) -> SimulationTimeTuple:
        return get_work_time_for_24_7_open_locations()
