from typing import Optional, Sequence, List

from .base import BasePerson
from .routine_utils import execute_routines
from ..interfaces import PersonRoutineWithStatus, PersonState, LocationID, SimulationTime, NoOP, SimulationTimeTuple, \
    NOOP, PersonRoutine, ContactTracer, PersonID


class Student(BasePerson):
    """Class that implements a school going minor."""

    _university: Optional[LocationID] = None
    _university_time: SimulationTimeTuple

    _routines: List[PersonRoutine]
    _outside_university_rs: List[PersonRoutineWithStatus]

    def __init__(self,
                 person_id: PersonID,
                 home: LocationID,
                 university: Optional[LocationID] = None,
                 university_time: Optional[SimulationTimeTuple] = None,
                 regulation_compliance_prob: float = 1.0,
                 init_state: Optional[PersonState] = None):
        """
        :param person_id: PersonID instance
        :param home: Home location id
        :param university: school location id
        :param university_time: school time specified in SimTimeTuples. Default - 9am-5pm and Mon-Fri
        :param regulation_compliance_prob: probability of complying to a regulation
        :param init_state: Optional initial state of the person
        """
        assert 18 < person_id.age <= 21, "A student's age should be <= 21"
        self._university = university
        self._university_time = university_time or SimulationTimeTuple(hours=tuple(range(9, 15)), week_days=tuple(range(0, 5)))
        self._routines = []
        self._outside_university_rs = []

        super().__init__(person_id=person_id,
                         home=home,
                         regulation_compliance_prob=regulation_compliance_prob,
                         init_state=init_state)

    @property
    def university(self) -> Optional[LocationID]:
        return self._university

    @property
    def assigned_locations(self) -> Sequence[LocationID]:
        if self._university is None:
            return self._home,
        else:
            return self._home, self._university

    @property
    def at_university(self) -> bool:
        """Return True if the person is at school and False otherwise"""
        return self.university is not None and self._state.current_location == self.university

    def set_outside_school_routines(self, routines: Sequence[PersonRoutine]) -> None:
        """A sequence of person routines to run outside school time"""
        for routine in routines:
            if routine not in self._routines:
                self._routines.append(routine)
                self._outside_university_rs.append(PersonRoutineWithStatus(routine))

    def _sync(self, sim_time: SimulationTime) -> None:
        super()._sync(sim_time)

        for rws in self._outside_university_rs:
            rws.sync(sim_time=sim_time, person_state=self.state)

    def step(self, sim_time: SimulationTime, contact_tracer: Optional[ContactTracer] = None) -> Optional[NoOP]:
        step_ret = super().step(sim_time, contact_tracer)
        if step_ret != NOOP:
            return step_ret

        if self.university is not None and sim_time in self._university_time:
            if not self.at_university and self.enter_location(self.university):
                return None
        else:
            ret = execute_routines(person=self, routines_with_status=self._outside_university_rs)
            if ret != NOOP:
                return ret

            if not self.at_home:
                self.enter_location(self.home)
                return None

        return NOOP

    def reset(self) -> None:
        super().reset()
        for rws in self._outside_university_rs:
            rws.reset()
