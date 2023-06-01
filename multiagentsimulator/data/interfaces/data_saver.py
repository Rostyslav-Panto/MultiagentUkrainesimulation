from abc import ABC
from typing import Any, Optional, Union

import numpy as np

from ...environment import PandemicObservation


class ExperimentDataSaver(ABC):

    def begin(self, obs: PandemicObservation) -> None:
        pass

    def record(self, obs: PandemicObservation, reward: Optional[Union[np.ndarray, float]] = None) -> None:
        pass

    def finalize(self, **kwargs: Any) -> bool:
        pass

    def close(self) -> None:
        pass
