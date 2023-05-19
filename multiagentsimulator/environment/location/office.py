
from dataclasses import dataclass

from ..interfaces import NonEssentialBusinessLocationState, ContactRate, SimulationTimeTuple, AgeRestrictedBusinessBaseLocation


@dataclass
class OfficeState(NonEssentialBusinessLocationState):
    contact_rate: ContactRate = ContactRate(2, 1, 0, 0.1, 0.01, 0.01)
    open_time: SimulationTimeTuple = SimulationTimeTuple(hours=tuple(range(9, 17)), week_days=tuple(range(0, 5)))


class Office(AgeRestrictedBusinessBaseLocation[OfficeState]):
    """Implements an office"""
    state_type = OfficeState
    age_limits = (18, 110)
