from typing import Optional, Sequence, List

from .base import BasePerson
from .routine_utils import execute_routines
from ..interfaces import PersonRoutineWithStatus, PersonState, LocationID, SimulationTime, NoOP, SimulationTimeTuple, \
    NOOP, PersonRoutine, ContactTracer, PersonID


class Child(BasePerson):

    _school: Optional[LocationID] = None
    _school_time: SimulationTimeTuple

    _routines: List[PersonRoutine]
    _outside_school_rs: List[PersonRoutineWithStatus]

    def __init__(self,
                 person_id: PersonID,
                 home: LocationID,
                 school: Optional[LocationID] = None,
                 school_time: Optional[SimulationTimeTuple] = None,
                 regulation_compliance_prob: float = 1.0,
                 init_state: Optional[PersonState] = None):
        assert person_id.age <= 18, "A minor's age should be <= 18"
        self._school = school
        self._school_time = school_time or SimulationTimeTuple(hours=tuple(range(9, 15)), week_days=tuple(range(0, 5)))
        self._routines = []
        self._outside_school_rs = []

        super().__init__(person_id=person_id,
                         home=home,
                         regulation_compliance_prob=regulation_compliance_prob,
                         init_state=init_state)

    @property
    def school(self) -> Optional[LocationID]:
        return self._school

    @property
    def assigned_locations(self) -> Sequence[LocationID]:
        if self._school is None:
            return self._home,
        else:
            return self._home, self._school

    @property
    def at_school(self) -> bool:
        return self.school is not None and self._state.current_location == self.school

    def set_outside_school_routines(self, routines: Sequence[PersonRoutine]) -> None:
        for routine in routines:
            if routine not in self._routines:
                self._routines.append(routine)
                self._outside_school_rs.append(PersonRoutineWithStatus(routine))

    def _sync(self, sim_time: SimulationTime) -> None:
        super()._sync(sim_time)

        for rws in self._outside_school_rs:
            rws.sync(sim_time=sim_time, person_state=self.state)

    def step(self, sim_time: SimulationTime, contact_tracer: Optional[ContactTracer] = None) -> Optional[NoOP]:
        step_ret = super().step(sim_time, contact_tracer)
        if step_ret != NOOP:
            return step_ret

        if self.school is not None and sim_time in self._school_time:
            # school time - go to school
            if not self.at_school and self.enter_location(self.school):
                return None
        else:
            # execute outside school routines
            ret = execute_routines(person=self, routines_with_status=self._outside_school_rs)
            if ret != NOOP:
                return ret

            # if not at home go home
            if not self.at_home:
                self.enter_location(self.home)
                return None

        return NOOP

    def reset(self) -> None:
        super().reset()
        for rws in self._outside_school_rs:
            rws.reset()
