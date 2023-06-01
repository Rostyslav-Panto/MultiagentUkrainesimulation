from dataclasses import dataclass

from ..interfaces import NonEssentialBusinessLocationState, ContactRate, SimulationTimeTuple, UnnecessaryBusinessBaseLocation

@dataclass
class SchoolState(NonEssentialBusinessLocationState):
    contact_rate: ContactRate = ContactRate(5, 1, 0, 0.1, 0., 0.1)
    open_time: SimulationTimeTuple = SimulationTimeTuple(hours=tuple(range(7, 15)), week_days=tuple(range(0, 5)))


class School(UnnecessaryBusinessBaseLocation[SchoolState]):

    state_type = SchoolState
