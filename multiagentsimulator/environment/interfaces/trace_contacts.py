
from abc import ABC, abstractmethod
from typing import Mapping

import numpy as np
from orderedset import OrderedSet

from .ids import PersonID


class ContactTracer(ABC):

    @abstractmethod
    def new_time_slot(self) -> None:

        pass

    @abstractmethod
    def reset(self) -> None:

        pass

    @abstractmethod
    def add_contacts(self, contacts: OrderedSet) -> None:

        pass

    @abstractmethod
    def get_contacts(self, person_id: PersonID) -> Mapping[PersonID, np.ndarray]:

        pass
