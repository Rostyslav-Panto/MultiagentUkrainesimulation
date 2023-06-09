
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Optional, Sequence, List, Tuple

from .trace_contacts import ContactTracer
from .ids import PersonID, LocationID
from .model import IndividualInfectionState, Risk
from .pandemic_testing_result import PandemicTestResult
from .pandemic_types import NoOP
from .regulation import ChosenRegulation
from .simulation_time import SimulationTime



@dataclass
class PersonState:
    """State of the person."""
    current_location: LocationID
    risk: Risk
    infection_state: Optional[IndividualInfectionState] = None
    infection_spread_multiplier: float = 1.

    quarantine: bool = field(init=False, default=False)
    quarantine_if_contact_positive: bool = field(init=False, default=False)
    quarantine_if_household_quarantined: bool = field(init=False, default=False)
    sick_at_home: bool = field(init=False, default=False)
    avoid_gathering_size: int = field(init=False, default=-1)

    test_result: PandemicTestResult = field(init=False, default=PandemicTestResult.UNTESTED)

    avoid_location_types: List[type] = field(default_factory=list, init=False)
    not_infection_probability: float = field(default=1., init=False)
    not_infection_probability_history: List[Tuple[LocationID, float]] = field(default_factory=list, init=False)


class Person(ABC):

    @abstractmethod
    def step(self, sim_time: SimulationTime, contact_tracer: Optional[ContactTracer] = None) -> Optional[NoOP]:

        pass

    @abstractmethod
    def receive_regulation(self, regulation: ChosenRegulation) -> None:
        """
        Receive a regulation that can potentially update the person's policy.

        :param regulation: a PandemicRegulation instance
        """
        pass

    @abstractmethod
    def enter_location(self, location_id: LocationID) -> bool:
        """
        Enter a location.

        :param location_id: LocationID instance
        :return: True if successful else False
        """
        pass

    @property
    @abstractmethod
    def id(self) -> PersonID:
        """
        Method that returns the id of the person.

        :return: ID of the person.
        """
        pass

    @property
    @abstractmethod
    def home(self) -> LocationID:
        """
        Property that returns the person's home location id.

        :return: ID of the home location
        """
        pass

    @property
    @abstractmethod
    def assigned_locations(self) -> Sequence[LocationID]:
        """
        Property that returns a sequence of location ids that the person is assigned to.

        :return: A collection of LocationIDs
        """

    @property
    @abstractmethod
    def state(self) -> PersonState:
        """
        Property that returns the current state of the person.

        :return: Current state of the person.
        """
        pass

    @abstractmethod
    def reset(self) -> None:
        """Reset person to its initial state."""
