
from dataclasses import dataclass

from ..interfaces import NonEssentialBusinessLocationState, ContactRate, SimulationTimeTuple, \
    AgeRestrictedBusinessBaseLocation, UnnecessaryBusinessBaseLocation


@dataclass
class RestaurantState(NonEssentialBusinessLocationState):
    contact_rate: ContactRate = ContactRate(1, 1, 0, 0.7, 0.25, 0.1)
    open_time: SimulationTimeTuple = SimulationTimeTuple(hours=tuple(range(11, 16)) + tuple(range(19, 24)),
                                                         week_days=tuple(range(1, 7)))


class Restaurant(UnnecessaryBusinessBaseLocation[RestaurantState]):
    """Implements a restaurant location."""
    state_type = RestaurantState
