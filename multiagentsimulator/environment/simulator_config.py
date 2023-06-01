import dataclasses
from dataclasses import dataclass, field
from typing import Sequence, Type, Any, Dict, Optional, List

from geopandas import GeoDataFrame

from .interfaces import BaseLocation, PersonRoutineAssignment
from .location import Hospital, HospitalState


@dataclass
class LocationConfigs:
    location_type: Type[BaseLocation]

    num: int

    num_assignees: int = -1

    positions: GeoDataFrame = field(default_factory=list)

    state_opts: Dict[str, Any] = field(default_factory=dict)

    extra_opts: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for k in self.state_opts:
            assert k in [f.name for f in dataclasses.fields(self.location_type.state_type)]


@dataclass
class SimulationConfigs:

    num_persons: int = 1000

    location_configs: Sequence[LocationConfigs] = ()

    regulation_compliance_prob: float = 0.99

    max_hospital_capacity: int = field(init=False, default=-1)

    person_routine_assignment: Optional[PersonRoutineAssignment] = None

    def __post_init__(self) -> None:
        for config in self.location_configs:
            if issubclass(config.location_type, Hospital):
                patient_capacity = config.state_opts.get('patient_capacity', HospitalState.patient_capacity)
                self.max_hospital_capacity = config.num * patient_capacity
