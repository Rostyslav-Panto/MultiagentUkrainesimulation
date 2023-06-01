
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Optional



class InfectionSummary(Enum):
    NONE = 'none (N)'
    INFECTED = 'infected (I)'
    CRITICAL = 'critical (C)'
    RECOVERED = 'recovered (R)'
    DEAD = 'dead (D)'


sorted_infection_summary = sorted(InfectionSummary, key=lambda x: x.value)


class Risk(Enum):
    LOW = 0
    HIGH = 1


@dataclass(frozen=True)
class IndividualInfectionState:
    summary: InfectionSummary
    spread_probability: float
    exposed_rnb: float = -1.
    is_hospitalized: bool = False
    shows_symptoms: bool = False


class InfectionModel(ABC):

    @abstractmethod
    def step(self, subject_infection_state: Optional[IndividualInfectionState], subject_age: int,
             subject_risk: Risk, infection_probability: float) -> IndividualInfectionState:

        pass

    @abstractmethod
    def needs_contacts(self, subject_infection_state: Optional[IndividualInfectionState]) -> bool:

        pass

    @abstractmethod
    def reset(self) -> None:
        pass
