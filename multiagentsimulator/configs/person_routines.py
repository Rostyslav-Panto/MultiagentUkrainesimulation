

from typing import Sequence, Type

from ..environment import LocationID, PersonRoutine, University, Restaurant, \
    Store, triggered_routine, weekend_routine, social_routine, mid_day_during_week_routine, \
    PersonRoutineAssignment, Person, Retired, Child, Adult, Location


class DefaultPersonRoutineAssignment(PersonRoutineAssignment):

    @property
    def required_location_types(self) -> Sequence[Type[Location]]:
        return University, Restaurant, Store

    @staticmethod
    def get_minor_routines(home_id: LocationID, age: int) -> Sequence[PersonRoutine]:
        routines = [
            triggered_routine(home_id, University, 30),
            weekend_routine(home_id, Restaurant, explore_probability=0.5),
        ]
        if age >= 12:
            routines.append(social_routine(home_id))

        return routines

    @staticmethod
    def get_retired_routines(home_id: LocationID) -> Sequence[PersonRoutine]:
        routines = [
            triggered_routine(None, Store, 7),
            triggered_routine(None, University, 30),
            weekend_routine(None, Restaurant, explore_probability=0.5),
            social_routine(home_id)
        ]
        return routines

    @staticmethod
    def get_worker_during_work_routines(work_id: LocationID) -> Sequence[PersonRoutine]:
        routines = [
            mid_day_during_week_routine(work_id, Restaurant),  # ~cafeteria  during work
        ]

        return routines

    @staticmethod
    def get_worker_outside_work_routines(home_id: LocationID) -> Sequence[PersonRoutine]:
        routines = [
            triggered_routine(None, Store, 7),
            triggered_routine(None, University, 30),
            weekend_routine(None, Restaurant, explore_probability=0.5),
            social_routine(home_id)
        ]
        return routines

    def assign_routines(self, persons: Sequence[Person]) -> None:
        for p in persons:
            if isinstance(p, Retired):
                p.set_routines(self.get_retired_routines(p.home))
            elif isinstance(p, Child):
                p.set_outside_school_routines(self.get_minor_routines(p.home, p.id.age))
            elif isinstance(p, Adult):
                p.set_during_work_routines(self.get_worker_during_work_routines(p.work))
                p.set_outside_work_routines(self.get_worker_outside_work_routines(p.home))
