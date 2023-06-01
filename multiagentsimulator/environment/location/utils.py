
from ..interfaces import globals, SimulationTimeTuple


def get_work_time_for_24_7_open_locations() -> SimulationTimeTuple:
    if globals.numpy_rng.random() < 0.5:
        hours = (22, 23) + tuple(range(0, 7))
    else:
        start = globals.numpy_rng.randint(7, 13)
        hours = tuple(range(start, start + 9))

    start = globals.numpy_rng.randint(0, 2)
    week_days = tuple(range(start, start + 6))
    return SimulationTimeTuple(hours, week_days)
