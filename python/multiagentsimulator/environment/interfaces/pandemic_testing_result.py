
from enum import IntEnum



class PandemicTestResult(IntEnum):
    UNTESTED = 0
    NEGATIVE = 1
    POSITIVE = 2
    CRITICAL = 3
    DEAD = 4
