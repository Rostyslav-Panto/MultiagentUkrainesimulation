
from typing import Optional, Sequence, List

from .base import BasePerson
from .routine_utils import execute_routines
from ..interfaces import LocationID, SimulationTime, NoOP, NOOP, PersonState, PersonRoutine, ContactTracer, PersonID, \
    PersonRoutineWithStatus


class Retired(BasePerson):

    _routines: List[PersonRoutine]
    _routines_with_status: List[PersonRoutineWithStatus]

    def __init__(self,
                 person_id: PersonID,
                 home: LocationID,
                 regulation_compliance_prob: float = 1.0,
                 init_state: Optional[PersonState] = None):

        self._routines = []
        self._routines_with_status = []

        super().__init__(person_id=person_id,
                         home=home,
                         regulation_compliance_prob=regulation_compliance_prob,
                         init_state=init_state)

    def _sync(self, sim_time: SimulationTime) -> None:
        super()._sync(sim_time)

        for rws in self._routines_with_status:
            rws.sync(sim_time=sim_time, person_state=self.state)

    def set_routines(self, routines: Sequence[PersonRoutine]) -> None:
        for routine in routines:
            if routine not in self._routines:
                self._routines.append(routine)
                self._routines_with_status.append(PersonRoutineWithStatus(routine))

    def step(self, sim_time: SimulationTime, contact_tracer: Optional[ContactTracer] = None) -> Optional[NoOP]:
        step_ret = super().step(sim_time, contact_tracer)
        if step_ret != NOOP:
            return step_ret

        # execute routines
        ret = execute_routines(person=self, routines_with_status=self._routines_with_status)
        if ret != NOOP:
            return ret

        # if not at home go home
        if not self.at_home:
            self.enter_location(self.home)
            return None

        return NOOP

    def reset(self) -> None:
        super().reset()
        for rws in self._routines_with_status:
            rws.reset()
