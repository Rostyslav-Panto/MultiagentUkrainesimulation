from collections import defaultdict
from dataclasses import dataclass, field
from typing import Dict, Any, Optional, Union, List, Type

from .pandemic_types import Default


from .model import Risk


@dataclass(frozen=True)
class ChosenRegulation:
    location_type_to_rule_kwargs: Optional[Dict[Type, Dict[str, Any]]] = None
    business_type_to_rule_kwargs: Optional[Dict[Type, Dict[str, Any]]] = None
    social_distancing: Union[float, Default, None] = None
    quarantine: bool = False
    quarantine_if_contact_positive: bool = False
    quarantine_if_household_quarantined: bool = False
    stay_home_if_sick: bool = False
    practice_good_hygiene: bool = False
    wear_facial_coverings: bool = False
    risk_to_avoid_gathering_size: Dict[Risk, int] = field(default_factory=lambda: defaultdict(lambda: -1))
    risk_to_avoid_location_types: Optional[Dict[Risk, List[type]]] = None
    stage: int = 0
