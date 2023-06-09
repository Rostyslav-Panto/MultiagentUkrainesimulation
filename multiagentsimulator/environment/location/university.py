from dataclasses import dataclass

from ..interfaces import NonEssentialBusinessLocationState, ContactRate, SimulationTimeTuple, UnnecessaryBusinessBaseLocation


@dataclass
class UniversityState(NonEssentialBusinessLocationState):
    contact_rate: ContactRate = ContactRate(1, 1, 0, 0.5, 0.3, 0.1)
    open_time: SimulationTimeTuple = SimulationTimeTuple(hours=tuple(range(9, 17)), week_days=tuple(range(1, 7)))


class University(UnnecessaryBusinessBaseLocation[UniversityState]):
    state_type = UniversityState
