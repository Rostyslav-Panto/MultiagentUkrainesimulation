from typing import Optional

import numpy as np

from .registry import Registry

registry: Optional[Registry] = None
numpy_rng: np.random.RandomState = np.random.RandomState()
