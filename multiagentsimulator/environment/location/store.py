from dataclasses import dataclass

from ..interfaces import BusinessLocationState, ContactRate, SimulationTimeTuple, NonEssentialBusinessLocationState, \
    ImportantBusinessBaseLocation, NoImportantBusinessBaseLocation

@dataclass
class GroceryStoreState(BusinessLocationState):
    contact_rate: ContactRate = ContactRate(0, 1, 0, 0.2, 0.25, 0.3)
    open_time: SimulationTimeTuple = SimulationTimeTuple(hours=tuple(range(7, 21)), week_days=tuple(range(0, 6)))


class GroceryStore(ImportantBusinessBaseLocation[GroceryStoreState]):
    """Implements a grocery store location."""

    state_type = GroceryStoreState


@dataclass
class RetailStoreState(NonEssentialBusinessLocationState):
    contact_rate: ContactRate = ContactRate(0, 1, 0, 0.2, 0.25, 0.3)
    open_time: SimulationTimeTuple = SimulationTimeTuple(hours=tuple(range(7, 21)), week_days=tuple(range(0, 6)))


class RetailStore(NoImportantBusinessBaseLocation[RetailStoreState]):
    """Implements a retail store location."""

    state_type = RetailStoreState
