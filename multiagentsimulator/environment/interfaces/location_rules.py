import dataclasses
from typing import Union, Optional, Type

from .location_states import ContactRate
from .pandemic_types import Default, DEFAULT
from .simulation_time import SimulationTimeTuple


@dataclasses.dataclass(frozen=True)
class LocationRule:
    contact_rate: Union[ContactRate, Default, None] = None
    visitor_time: Union[SimulationTimeTuple, Default, None] = None
    visitor_capacity: Union[Default, int, None] = None

    @classmethod
    def get_default(cls: Type['LocationRule']) -> 'LocationRule':
        return LocationRule(**{f.name: DEFAULT for f in dataclasses.fields(cls)})


@dataclasses.dataclass(frozen=True)
class BusinessLocationRule(LocationRule):
    open_time: Union[SimulationTimeTuple, Default, None] = None


@dataclasses.dataclass(frozen=True)
class NonEssentialBusinessLocationRule(BusinessLocationRule):
    lock: Optional[bool] = None
