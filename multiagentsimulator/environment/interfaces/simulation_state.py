
from dataclasses import dataclass
from typing import Dict, Mapping, Tuple, Type

from .ids import LocationID, PersonID
from .model import InfectionSummary
from .location import LocationSummary
from .location_states import LocationState
from .pandemic_testing import GlobalTestingState
from .person import PersonState
from .simulation_time import SimulationTime


@dataclass
class SimulationState:

    id_to_person_state: Dict[PersonID, PersonState]

    id_to_location_state: Dict[LocationID, LocationState]

    location_type_infection_summary: Dict[Type, int]

    global_infection_summary: Dict[InfectionSummary, int]

    global_testing_state: GlobalTestingState

    global_location_summary: Mapping[Tuple[str, str], LocationSummary]

    infection_above_threshold: bool

    regulation_stage: int

    sim_time: SimulationTime
