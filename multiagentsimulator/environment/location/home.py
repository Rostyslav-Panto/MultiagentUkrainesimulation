
from dataclasses import dataclass

from ..interfaces import LocationState, ContactRate, SimulationTime, SimulationTimeTuple, LocationRule, globals, BaseLocation


@dataclass
class HomeState(LocationState):
    contact_rate: ContactRate = ContactRate(0, 1, 0, 0.5, 0.3, 0.3)
    visitor_time = SimulationTimeTuple(hours=tuple(range(15, 20)), days=tuple(globals.numpy_rng.randint(0, 365, 12)))


class Home(BaseLocation[HomeState]):
    state_type = HomeState

    def sync(self, sim_time: SimulationTime) -> None:
        super().sync(sim_time)
        self._state.social_gathering_event = sim_time in self._state.visitor_time

    def update_rules(self, new_rule: LocationRule) -> None:
        pass
