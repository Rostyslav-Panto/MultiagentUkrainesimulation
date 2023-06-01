from structlog import BoundLogger

from .city_registry import *
from .trace_contacts import *
from .finish import *
from .model import *
from .interfaces import *
from .job_recruiter import *
from .location import *
from .generate_population import *
from .simulation_environment import *
from .simulator import *
from .pandemic_testing_strategies import *
from .person import *
from .reward import *
from .simulator_config import *
from .simulator_settings import *


def init_globals(registry: Optional[Registry] = None,
                 seed: Optional[int] = None,
                 log: Optional[BoundLogger] = None) -> None:
    """
    Initialize globals for the simulator

    :param registry: Registry instance for the environment
    :param seed: numpy random seed
    :param log: optional logger
    :return: None
    """
    globals.registry = registry or CityRegistry()
    globals.numpy_rng = np.random.RandomState(seed)
    if log:
        log.info('Initialized globals for the simulator')
