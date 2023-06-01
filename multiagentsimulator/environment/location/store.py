from dataclasses import dataclass

from ..interfaces import BusinessLocationState, ContactRate, SimulationTimeTuple, NonEssentialBusinessLocationState, \
    NecessaryBusinessBaseLocation, UnnecessaryBusinessBaseLocation

@dataclass
class StoreState(BusinessLocationState):
    contact_rate: ContactRate = ContactRate(0, 1, 0, 0.2, 0.25, 0.3)
    open_time: SimulationTimeTuple = SimulationTimeTuple(hours=tuple(range(7, 21)), week_days=tuple(range(0, 6)))


class Store(NecessaryBusinessBaseLocation[StoreState]):

    state_type = StoreState

